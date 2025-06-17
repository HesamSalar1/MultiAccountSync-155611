
import json
import asyncio
import sys
import sqlite3
import logging
from datetime import datetime
import os
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from pyrogram import Client, filters
from pyrogram.types import Message, ChatMember
from pyrogram.errors import FloodWait, UserNotParticipant, ChatWriteForbidden
from random import choice

# تنظیم لاگینگ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('unified_bots.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class UnifiedBotLauncher:
    def __init__(self):
        self.bots = {}
        self.running = False
        
        # تنظیمات بات‌ها
        self.bot_configs = {
            1: {
                'api_id': 15508294,
                'api_hash': "778e5cd56ffcf22c2d62aa963ce85a0c",
                'session_name': "bots/bot1/my_bot1",
                'db_path': "bots/bot1/bot1_data.db",
                'log_path': "bots/bot1/bot1.log"
            },
            2: {
                'api_id': 15508294,
                'api_hash': "778e5cd56ffcf22c2d62aa963ce85a0c",
                'session_name': "bots/bot2/my_bot2",
                'db_path': "bots/bot2/bot2_data.db",
                'log_path': "bots/bot2/bot2.log"
            },
            3: {
                'api_id': 15508294,
                'api_hash': "778e5cd56ffcf22c2d62aa963ce85a0c",
                'session_name': "bots/bot3/my_bot3",
                'db_path': "bots/bot3/bot3_data.db",
                'log_path': "bots/bot3/bot3.log"
            },
            4: {
                'api_id': 15508294,
                'api_hash': "778e5cd56ffcf22c2d62aa963ce85a0c",
                'session_name': "bots/bot4/my_bot4",
                'db_path': "bots/bot4/bot4_data.db",
                'log_path': "bots/bot4/bot4.log"
            },
            5: {
                'api_id': 15508294,
                'api_hash': "778e5cd56ffcf22c2d62aa963ce85a0c",
                'session_name': "bots/bot5/my_bot5",
                'db_path': "bots/bot5/bot5_data.db",
                'log_path': "bots/bot5/bot5.log"
            },
            6: {
                'api_id': 15508294,
                'api_hash': "778e5cd56ffcf22c2d62aa963ce85a0c",
                'session_name': "bots/bot6/my_bot6",
                'db_path': "bots/bot6/bot6_data.db",
                'log_path': "bots/bot6/bot6.log"
            },
            7: {
                'api_id': 15508294,
                'api_hash': "778e5cd56ffcf22c2d62aa963ce85a0c",
                'session_name': "bots/bot7/my_bot7",
                'db_path': "bots/bot7/bot7_data.db",
                'log_path': "bots/bot7/bot7.log"
            },
            8: {
                'api_id': 15508294,
                'api_hash': "778e5cd56ffcf22c2d62aa963ce85a0c",
                'session_name': "bots/bot8/my_bot8",
                'db_path': "bots/bot8/bot8_data.db",
                'log_path': "bots/bot8/bot8.log"
            },
            9: {
                'api_id': 15508294,
                'api_hash': "778e5cd56ffcf22c2d62aa963ce85a0c",
                'session_name': "bots/bot9/my_bot9",
                'db_path': "bots/bot9/bot9_data.db",
                'log_path': "bots/bot9/bot9.log"
            }
        }
        
        self.admin_id = 7850529246

    def setup_database(self, bot_id, db_path):
        """تنظیم پایگاه داده برای هر بات"""
        try:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # ایجاد جداول مورد نیاز
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    join_date TEXT,
                    is_active INTEGER DEFAULT 1
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    message_text TEXT,
                    timestamp TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info(f"✅ پایگاه داده بات {bot_id} آماده شد")
            
        except Exception as e:
            logger.error(f"❌ خطا در تنظیم پایگاه داده بات {bot_id}: {e}")

    async def create_bot(self, bot_id, config):
        """ایجاد و تنظیم یک بات"""
        try:
            # تنظیم پایگاه داده
            self.setup_database(bot_id, config['db_path'])
            
            # ایجاد کلاینت
            app = Client(
                config['session_name'],
                api_id=config['api_id'],
                api_hash=config['api_hash']
            )
            
            # تعریف هندلرها
            @app.on_message(filters.command("start") & filters.private)
            async def start_command(client, message):
                try:
                    user_id = message.from_user.id
                    username = message.from_user.username or "بدون نام کاربری"
                    first_name = message.from_user.first_name or "نامشخص"
                    
                    # ذخیره در پایگاه داده
                    conn = sqlite3.connect(config['db_path'])
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        INSERT OR REPLACE INTO users 
                        (user_id, username, first_name, join_date, is_active)
                        VALUES (?, ?, ?, ?, 1)
                    ''', (user_id, username, first_name, datetime.now().isoformat()))
                    
                    conn.commit()
                    conn.close()
                    
                    welcome_msg = f"🤖 سلام {first_name}!\n\n✅ بات {bot_id} آماده خدمت رسانی است.\n\n📝 دستورات موجود:\n/start - شروع\n/help - راهنما\n/info - اطلاعات"
                    
                    await message.reply_text(welcome_msg)
                    logger.info(f"[بات {bot_id}] کاربر جدید: {username} ({user_id})")
                    
                except Exception as e:
                    logger.error(f"[بات {bot_id}] خطا در دستور start: {e}")

            @app.on_message(filters.command("help") & filters.private)
            async def help_command(client, message):
                help_text = f"""
🤖 راهنمای بات {bot_id}

📝 دستورات موجود:
/start - شروع و ثبت نام
/help - نمایش این راهنما
/info - اطلاعات بات

💡 برای دریافت پشتیبانی با ادمین تماس بگیرید.
                """
                await message.reply_text(help_text.strip())

            @app.on_message(filters.command("info") & filters.private)
            async def info_command(client, message):
                info_text = f"""
📊 اطلاعات بات {bot_id}

🆔 شناسه بات: {bot_id}
⚡ وضعیت: فعال
🕐 زمان راه‌اندازی: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
                await message.reply_text(info_text.strip())

            # دستورات مدیریتی ادمین (فقط برای بات 1)
            if bot_id == 1:
                @app.on_message(filters.command("status") & filters.user(self.admin_id))
                async def admin_status_command(client, message):
                    try:
                        status = self.get_status()
                        status_text = f"""
📊 **وضعیت لانچر واحد:**

🤖 تعداد کل بات‌ها: {status['total_bots']}
✅ بات‌های فعال: {status['running_bots']}
❌ بات‌های خطا: {status['error_bots']}

📋 **جزئیات بات‌ها:**
"""
                        
                        for bot_info in status['bots']:
                            emoji = "✅" if bot_info['status'] == 'running' else "❌"
                            status_text += f"{emoji} بات {bot_info['id']}: {bot_info['status']}\n"
                        
                        await message.reply_text(status_text.strip())
                        
                    except Exception as e:
                        await message.reply_text(f"❌ خطا: {e}")

                @app.on_message(filters.command("restart") & filters.user(self.admin_id))
                async def admin_restart_command(client, message):
                    try:
                        if len(message.command) < 2:
                            await message.reply_text("⚠️ استفاده: /restart [شماره_بات]\nمثال: /restart 2")
                            return
                        
                        bot_id = int(message.command[1])
                        if bot_id not in self.bot_configs:
                            await message.reply_text(f"❌ بات {bot_id} یافت نشد")
                            return
                        
                        await message.reply_text(f"🔄 راه‌اندازی مجدد بات {bot_id}...")
                        
                        success = await self.restart_bot(bot_id)
                        if success:
                            await message.reply_text(f"✅ بات {bot_id} مجدداً راه‌اندازی شد")
                        else:
                            await message.reply_text(f"❌ خطا در راه‌اندازی مجدد بات {bot_id}")
                        
                    except ValueError:
                        await message.reply_text("❌ شماره بات نامعتبر")
                    except Exception as e:
                        await message.reply_text(f"❌ خطا: {e}")

            @app.on_message(filters.text & filters.private & ~filters.command(["start", "help", "info", "status", "restart"]))
            async def handle_text_message(client, message):
                try:
                    user_id = message.from_user.id
                    message_text = message.text
                    
                    # ذخیره پیام در پایگاه داده
                    conn = sqlite3.connect(config['db_path'])
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        INSERT INTO messages (user_id, message_text, timestamp)
                        VALUES (?, ?, ?)
                    ''', (user_id, message_text, datetime.now().isoformat()))
                    
                    conn.commit()
                    conn.close()
                    
                    # پاسخ خودکار
                    responses = [
                        f"🤖 پیام شما در بات {bot_id} دریافت شد!",
                        f"✅ پیام شما ثبت شد. (بات {bot_id})",
                        f"📝 متشکریم از ارسال پیام به بات {bot_id}",
                        f"🔔 پیام شما توسط بات {bot_id} پردازش شد"
                    ]
                    
                    response = choice(responses)
                    await message.reply_text(response)
                    
                    logger.info(f"[بات {bot_id}] پیام از {user_id}: {message_text[:50]}...")
                    
                except Exception as e:
                    logger.error(f"[بات {bot_id}] خطا در پردازش پیام: {e}")

            # ذخیره بات
            self.bots[bot_id] = {
                'client': app,
                'config': config,
                'status': 'initialized'
            }
            
            logger.info(f"✅ بات {bot_id} ایجاد شد")
            return app
            
        except Exception as e:
            logger.error(f"❌ خطا در ایجاد بات {bot_id}: {e}")
            return None

    async def start_all_bots(self):
        """شروع همه بات‌ها"""
        self.running = True
        logger.info("🚀 شروع لانچر واحد بات‌ها...")
        
        # ایجاد همه بات‌ها
        tasks = []
        for bot_id, config in self.bot_configs.items():
            logger.info(f"🔧 ایجاد بات {bot_id}...")
            bot = await self.create_bot(bot_id, config)
            if bot:
                tasks.append(self.start_single_bot(bot_id))
        
        # شروع همه بات‌ها به صورت موازی
        if tasks:
            logger.info(f"🎯 شروع {len(tasks)} بات...")
            await asyncio.gather(*tasks, return_exceptions=True)

    async def start_single_bot(self, bot_id):
        """شروع یک بات"""
        try:
            if bot_id not in self.bots:
                logger.error(f"❌ بات {bot_id} یافت نشد")
                return
            
            bot_info = self.bots[bot_id]
            client = bot_info['client']
            
            logger.info(f"🚀 شروع بات {bot_id}...")
            
            await client.start()
            bot_info['status'] = 'running'
            bot_info['start_time'] = datetime.now()
            
            logger.info(f"✅ بات {bot_id} آماده و در حال اجرا!")
            
            # مانیتورینگ و نگه داشتن بات زنده
            while self.running and bot_info['status'] == 'running':
                try:
                    # بررسی وضعیت اتصال
                    if not client.is_connected:
                        logger.warning(f"⚠️ بات {bot_id} اتصال قطع شده - تلاش برای اتصال مجدد...")
                        await client.start()
                    
                    await asyncio.sleep(10)  # بررسی هر 10 ثانیه
                    
                except Exception as monitor_error:
                    logger.error(f"❌ خطا در مانیتورینگ بات {bot_id}: {monitor_error}")
                    await asyncio.sleep(5)
            
        except Exception as e:
            logger.error(f"❌ خطا در شروع بات {bot_id}: {e}")
            if bot_id in self.bots:
                self.bots[bot_id]['status'] = 'error'
                
                # تلاش برای راه‌اندازی مجدد خودکار
                logger.info(f"🔄 تلاش برای راه‌اندازی مجدد خودکار بات {bot_id} در 30 ثانیه...")
                await asyncio.sleep(30)
                if self.running:
                    await self.restart_bot(bot_id)

    async def stop_single_bot(self, bot_id):
        """متوقف کردن یک بات"""
        try:
            if bot_id in self.bots:
                bot_info = self.bots[bot_id]
                if bot_info['status'] == 'running':
                    logger.info(f"⏹️ متوقف کردن بات {bot_id}...")
                    await bot_info['client'].stop()
                    bot_info['status'] = 'stopped'
                    logger.info(f"✅ بات {bot_id} متوقف شد")
        except Exception as e:
            logger.error(f"❌ خطا در متوقف کردن بات {bot_id}: {e}")

    async def stop_all_bots(self):
        """متوقف کردن همه بات‌ها"""
        logger.info("🛑 متوقف کردن همه بات‌ها...")
        self.running = False
        
        tasks = []
        for bot_id in list(self.bots.keys()):
            tasks.append(self.stop_single_bot(bot_id))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def restart_bot(self, bot_id):
        """راه‌اندازی مجدد یک بات"""
        try:
            logger.info(f"🔄 راه‌اندازی مجدد بات {bot_id}...")
            
            # متوقف کردن بات فعلی
            await self.stop_single_bot(bot_id)
            await asyncio.sleep(2)
            
            # ایجاد مجدد بات
            if bot_id in self.bot_configs:
                config = self.bot_configs[bot_id]
                bot = await self.create_bot(bot_id, config)
                if bot:
                    # شروع مجدد بات
                    asyncio.create_task(self.start_single_bot(bot_id))
                    logger.info(f"✅ بات {bot_id} مجدداً راه‌اندازی شد")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ خطا در راه‌اندازی مجدد بات {bot_id}: {e}")
            return False

    def get_status(self):
        """دریافت وضعیت همه بات‌ها"""
        status = {
            'total_bots': len(self.bot_configs),
            'running_bots': len([b for b in self.bots.values() if b['status'] == 'running']),
            'error_bots': len([b for b in self.bots.values() if b['status'] == 'error']),
            'bots': []
        }
        
        for bot_id, bot_info in self.bots.items():
            status['bots'].append({
                'id': bot_id,
                'status': bot_info['status'],
                'config': bot_info['config']['session_name']
            })
        
        return status

# متغیر کلی لانچر
launcher = UnifiedBotLauncher()

async def main():
    """تابع اصلی"""
    try:
        print("="*60)
        print("🤖 لانچر واحد بات‌های تلگرام")
        print("="*60)
        print("🎯 شروع همه ۹ بات در یک فرآیند...")
        print("📍 برای متوقف کردن: Ctrl+C")
        print("="*60)
        
        # شروع همه بات‌ها
        await launcher.start_all_bots()
        
    except KeyboardInterrupt:
        logger.info("🔴 متوقف شدن با Ctrl+C")
    except Exception as e:
        logger.error(f"❌ خطای غیرمنتظره: {e}")
    finally:
        await launcher.stop_all_bots()

if __name__ == "__main__":
    asyncio.run(main())
