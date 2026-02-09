"""
AI Service
Groq va Gemini bilan ishlash, avtomatik fallback
"""
import json
from groq import Groq
import google.generativeai as genai
from typing import Optional, Dict, Tuple
import config

class AIService:
    """AI xizmatlari bilan ishlash"""
    
    def __init__(self):
        # Groq clientlar
        self.groq_client_1 = Groq(api_key=config.GROQ_API_KEY_1) if config.GROQ_API_KEY_1 else None
        self.groq_client_2 = Groq(api_key=config.GROQ_API_KEY_2) if config.GROQ_API_KEY_2 else None
        
        # Gemini
        if config.GEMINI_API_KEY:
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel(config.GEMINI_MODEL)
        else:
            self.gemini_model = None
        
        self.current_groq = 1  # Qaysi Groq ishlatilayotgani
    
    async def transcribe_voice(self, audio_file_path: str) -> Tuple[Optional[str], int]:
        """
        Ovozni matnga o'girish (Groq Whisper)
        Returns: (matn, ishlatilgan_tokenlar)
        """
        try:
            # Groq 1 bilan urinish
            if self.groq_client_1:
                try:
                    with open(audio_file_path, "rb") as audio_file:
                        transcription = self.groq_client_1.audio.transcriptions.create(
                            file=(audio_file_path, audio_file.read()),
                            model=config.GROQ_WHISPER_MODEL,
                            language="uz"  # O'zbek tili
                        )
                    return transcription.text, 1000  # Taxminiy token
                except Exception as e:
                    print(f"⚠️ Groq 1 Whisper xato: {e}")
            
            # Groq 2 bilan urinish
            if self.groq_client_2:
                try:
                    with open(audio_file_path, "rb") as audio_file:
                        transcription = self.groq_client_2.audio.transcriptions.create(
                            file=(audio_file_path, audio_file.read()),
                            model=config.GROQ_WHISPER_MODEL,
                            language="uz"
                        )
                    return transcription.text, 1000
                except Exception as e:
                    print(f"⚠️ Groq 2 Whisper xato: {e}")
            
            return None, 0
        
        except Exception as e:
            print(f"❌ Whisper xato: {e}")
            return None, 0
    
    async def analyze_transaction(self, text: str) -> Tuple[Optional[list], int]:
        """
        Moliyaviy matnni tahlil qilish (bir yoki bir nechta tranzaksiya)
        Returns: (tranzaksiyalar_ro'yxati, ishlatilgan_tokenlar)
        """
        prompt = config.TRANSACTION_ANALYSIS_PROMPT.format(text=text)
        
        # Groq 1 bilan urinish
        result, tokens = await self._call_groq(prompt, self.groq_client_1)
        if result:
            parsed = self._parse_json_response(result)
            # Agar array bo'lmasa, array qilib qaytarish
            if parsed and not isinstance(parsed, list):
                parsed = [parsed]
            return parsed, tokens
        
        # Groq 2 bilan urinish
        result, tokens = await self._call_groq(prompt, self.groq_client_2)
        if result:
            parsed = self._parse_json_response(result)
            if parsed and not isinstance(parsed, list):
                parsed = [parsed]
            return parsed, tokens
        
        # Gemini bilan urinish
        result, tokens = await self._call_gemini(prompt)
        if result:
            parsed = self._parse_json_response(result)
            if parsed and not isinstance(parsed, list):
                parsed = [parsed]
            return parsed, tokens
        
        return None, 0
    
    async def analyze_diary(self, text: str) -> Tuple[Optional[str], int]:
        """
        Kundalik tahlili
        Returns: (tahlil, ishlatilgan_tokenlar)
        """
        prompt = config.DIARY_ANALYSIS_PROMPT.format(text=text)
        
        # Groq 1
        result, tokens = await self._call_groq(prompt, self.groq_client_1)
        if result:
            return result, tokens
        
        # Groq 2
        result, tokens = await self._call_groq(prompt, self.groq_client_2)
        if result:
            return result, tokens
        
        # Gemini
        result, tokens = await self._call_gemini(prompt)
        if result:
            return result, tokens
        
        return None, 0
    
    async def generate_report(self, report_type: str, data: Dict) -> Tuple[Optional[str], int]:
        """
        Hisobot yaratish
        Returns: (hisobot, ishlatilgan_tokenlar)
        """
        if report_type == "weekly":
            prompt = config.WEEKLY_REPORT_PROMPT.format(**data)
        elif report_type == "monthly":
            prompt = config.MONTHLY_REPORT_PROMPT.format(**data)
        else:
            return None, 0
        
        # Groq 1
        result, tokens = await self._call_groq(prompt, self.groq_client_1)
        if result:
            return result, tokens
        
        # Groq 2
        result, tokens = await self._call_groq(prompt, self.groq_client_2)
        if result:
            return result, tokens
        
        # Gemini
        result, tokens = await self._call_gemini(prompt)
        if result:
            return result, tokens
        
        return None, 0
    
    async def _call_groq(self, prompt: str, client: Optional[Groq]) -> Tuple[Optional[str], int]:
        """Groq API chaqirish"""
        if not client:
            return None, 0
        
        try:
            response = client.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            
            text = response.choices[0].message.content
            tokens = response.usage.total_tokens if hasattr(response, 'usage') else 500
            
            return text, tokens
        
        except Exception as e:
            print(f"⚠️ Groq API xato: {e}")
            return None, 0
    
    async def _call_gemini(self, prompt: str) -> Tuple[Optional[str], int]:
        """Gemini API chaqirish"""
        if not self.gemini_model:
            return None, 0
        
        try:
            response = self.gemini_model.generate_content(prompt)
            text = response.text
            tokens = 500  # Taxminiy
            
            return text, tokens
        
        except Exception as e:
            print(f"⚠️ Gemini API xato: {e}")
            return None, 0
    
    def _parse_json_response(self, text: str) -> Optional[Dict]:
        """JSON javobni parse qilish"""
        try:
            # Agar matnda ```json``` bo'lsa, uni olib tashlash
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            return json.loads(text)
        except Exception as e:
            print(f"⚠️ JSON parse xato: {e}")
            # Oddiy regex bilan parse qilishga urinish
            try:
                import re
                amount_match = re.search(r'"amount":\s*(\d+)', text)
                type_match = re.search(r'"type":\s*"(\w+)"', text)
                category_match = re.search(r'"category":\s*"([^"]+)"', text)
                
                if amount_match and type_match:
                    return {
                        "amount": int(amount_match.group(1)),
                        "type": type_match.group(1),
                        "category": category_match.group(1) if category_match else "Boshqa",
                        "description": ""
                    }
            except:
                pass
            
            return None
