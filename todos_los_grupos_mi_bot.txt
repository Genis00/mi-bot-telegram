# todos_los_grupos_mi_bot.py
import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ---------------------------
# Config desde variables de entorno
# ---------------------------
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
# SESSION_STRING: string session generado localmente y guardado en Render (no subir a git)
SESSION_STRING = os.getenv("SESSION_STRING", "")
# Nombre de sesión por defecto si quieres crear una localmente (no se usa en Render)
SESSION_NAME = os.getenv("SESSION_NAME", "mi_sesion")

# Canal destino (puede ser username como @miCanal o ID -100...)
CANAL_DESTINO = os.getenv("CANAL_DESTINO", "🔥VIP of VIPs | Binary Options💰")

# Lista de grupos: pasados por variable de entorno como IDs separados por comas.
# Ejemplo: -1002397356418,-4888064480,-1002147108799
GRUPOS_ENV = os.getenv("GRUPOS_IDS", "")
if GRUPOS_ENV:
    grupos_ids = [int(x.strip()) for x in GRUPOS_ENV.split(",") if x.strip()]
else:
    # Fallback (tu lista original)
    grupos_ids = [
        -1002397356418,  # SECRET CHAT: POCKET TRADING
        -4888064480,     # Mi grupo
        -1002147108799,  # BWG VIP 💎
        -1002670130705,  # LEGEND POCKET COMPOUNDING💸
        -1002511692719   # LEGEND POCKET VIP📈
    ]

# ---------------------------
# SCRIPT PRINCIPAL
# ---------------------------
ultimo_grupo = None  # Guardará el ID del último grupo que envió un mensaje

def build_client():
    """Crea el client usando StringSession si SESSION_STRING está presente, si no usa file session."""
    if SESSION_STRING:
        return TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    else:
        # Si no hay SESSION_STRING, usa una session file (no recomendado en Render)
        return TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def main():
    client = build_client()
    await client.start()
    print("✅ Bot conectado a Telegram correctamente.\n")

    # Resolver canal destino (acepta username o ID)
    try:
        destino_entity = await client.get_entity(CANAL_DESTINO)
        print(f"📍 Canal destino resuelto: {destino_entity.title if hasattr(destino_entity, 'title') else destino_entity}")
    except Exception:
        # Si falla, lo dejamos en raw (Telethon puede aceptar ID o username directamente más tarde)
        destino_entity = CANAL_DESTINO
        print(f"⚠️ No se pudo resolver el canal destino automáticamente, usando: {CANAL_DESTINO}")

    # Mostrar grupos detectados
    print("📍 Grupos detectados:")
    for g in grupos_ids:
        print(f" - {g}")
    print(f"\n🚀 Reenviando todos los mensajes al canal: {CANAL_DESTINO}\n")

    @client.on(events.NewMessage(chats=grupos_ids))
    async def handler(event):
        global ultimo_grupo
        try:
            chat = await event.get_chat()
            nombre_grupo = getattr(chat, "title", str(chat.id))
        except Exception:
            nombre_grupo = "Grupo desconocido"

        try:
            # Si el mensaje proviene de un grupo distinto al anterior, enviar encabezado (opcional)
            if ultimo_grupo != getattr(chat, "id", None):
                encabezado = f"💬 {nombre_grupo}"
                try:
                    await client.send_message(destino_entity, encabezado)
                except Exception:
                    # fallback: usar CANAL_DESTINO crudo
                    await client.send_message(CANAL_DESTINO, encabezado)
                ultimo_grupo = getattr(chat, "id", None)

            # ✅ Reenviar el mensaje original (manteniendo origen y formato)
            # forward_messages acepta: (entity, messages, from_peer=None)
            await client.forward_messages(destino_entity, event.message)
        except Exception as e:
            print(f"⚠️ Error reenviando mensaje desde {nombre_grupo}: {e}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
