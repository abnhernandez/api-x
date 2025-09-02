import tweepy
import time
import random
import os
import json
import datetime
from dotenv import load_dotenv

# FastAPI para exponer el servicio como web
from fastapi import FastAPI, BackgroundTasks
import uvicorn

# Cargar credenciales desde .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Validar que todas las credenciales estén presentes
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
    print("❌ Error: Faltan credenciales en el archivo .env")
    print("Asegúrate de tener: API_KEY, API_SECRET, "
          "ACCESS_TOKEN, ACCESS_SECRET")
    exit(1)

# Configurar cliente para API v2
try:
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET,
        wait_on_rate_limit=True
    )
    # Verificar credenciales
    me = client.get_me()
    print(f"✅ Conectado como: @{me.data.username}")
except Exception as e:
    print(f"❌ Error al conectar con Twitter: {e}")
    exit(1)

# Lista completa con 100 tweets de exhortación y mini enseñanza
tweets = [
    # 1–20: Libertad en Cristo
    ("🕊 'Donde está el Espíritu del Señor, allí hay libertad.' — "
     "2 Corintios 3:17\n¿En qué áreas de tu vida necesitas dejar que "
     "el Espíritu te libere? Reflexiona hoy."),

    ("La verdadera libertad comienza en el alma. No te dejes atar por "
     "miedos ni culpas. Cristo rompe cadenas.\n'Si el Hijo los hace "
     "libres, serán verdaderamente libres.' — Juan 8:36"),

    ("No permitas que el rencor aprisione tu corazón. El perdón es la "
     "llave para ser libre. ¿A quién necesitas perdonar hoy?"),

    ("La libertad de Cristo no es solo para hoy, es para siempre. "
     "Confía en que Su Espíritu te guía hacia vida plena."),

    ("¿Qué pensamientos o hábitos te tienen atado? Entrégaselos a Dios "
     "y recibe Su poder para vencer."),

    ("Libérate de la mentira de que no puedes cambiar. En Cristo, "
     "todo es posible. Cree y avanza."),

    ("La libertad no es hacer lo que quieras, sino hacer lo que Dios "
     "quiere en ti. Esa libertad trae paz verdadera."),

    ("Cuando dejas que Dios gobierne tu corazón, el temor pierde poder. "
     "La libertad nace en la confianza."),

    ("Jesús te invita a vivir sin miedo, sin cadenas internas. "
     "¿Estás dispuesto a entregarle todo?"),

    ("'El que practica el pecado es esclavo del pecado.' (Juan 8:34) "
     "Hoy decide caminar en libertad y no en esclavitud."),

    ("No permitas que el pasado controle tu presente. Dios hace nuevas "
     "todas las cosas y te ofrece libertad real."),

    ("La libertad cristiana es un llamado a la responsabilidad y a "
     "vivir en obediencia amorosa."),

    ("El Espíritu Santo te da poder para vencer las ataduras del mundo "
     "y de ti mismo. Ábrete a esa gracia."),

    ("La verdadera libertad es fruto de una relación profunda con "
     "Cristo, no de esfuerzos humanos."),

    ("El primer paso para ser libre es reconocer la necesidad de Dios. "
     "¿Lo has hecho hoy?"),

    ("En la cruz Jesús pagó el precio para que fueras libre de culpa "
     "y condena. Recibe esa libertad con fe."),

    ("No ignores la voz del Espíritu que te llama a liberarte de todo "
     "lo que te limita."),

    ("La libertad no es ausencia de pruebas, sino presencia de Dios "
     "en medio de ellas."),

    ("Camina hoy en libertad: suelta el control y confía en el plan "
     "de Dios para ti."),

    ("Recuerda: donde hay Espíritu Santo, hay vida y libertad. "
     "Ábrele la puerta a tu corazón."),

    # 21–40: Fortaleza en Dios
    ("🌾 'Los que confían en el Señor son como el monte de Sion, que no "
     "se mueve.' — Salmo 125:1\nConfía y permanece firme aunque la "
     "tormenta ruja."),

    ("Dios es tu roca eterna. En Él encontrarás fuerza para no caer "
     "ni rendirte."),

    ("La fe firme no es ausencia de dudas, sino decisión de confiar "
     "a pesar de ellas."),

    ("Cuando todo parece incierto, recuerda que Dios es tu refugio "
     "seguro."),

    ("No te desalientes por la debilidad; es oportunidad para que Dios "
     "muestre Su poder."),

    ("En medio del caos, Dios sostiene a los que le buscan con corazón "
     "sincero."),

    ("La confianza en Dios es el ancla que evita que tu alma "
     "naufrague."),

    ("Cuando te sientas débil, recuerda que Su poder se perfecciona "
     "en tu debilidad."),

    ("No te muevas por las circunstancias, sino por la verdad de "
     "Su Palabra."),

    ("La fidelidad de Dios es eterna; pon tu esperanza en Él "
     "sin vacilar."),

    ("'No temas, porque yo estoy contigo.' — Isaías 41:10. "
     "Dios es tu fortaleza."),

    ("La confianza en Dios se cultiva cada día con oración y "
     "meditación en Su Palabra."),

    ("Los que esperan en el Señor renuevan sus fuerzas. "
     "¿Estás dispuesto a esperar?"),

    "Dios nunca falla. Aunque falles tú, Él permanece firme.",

    ("Pon tus cargas en las manos de Dios y Él te dará descanso "
     "y fortaleza."),

    ("La fortaleza del creyente nace en la comunión diaria "
     "con Dios."),

    ("Ante la adversidad, no mires lo que pierdes, sino a quién "
     "tienes: Dios contigo."),

    ("La paciencia en las pruebas fortalece tu fe y produce "
     "esperanza."),

    ("La roca que sostiene tu vida no es la suerte ni tu esfuerzo, "
     "sino Dios."),

    ("En los momentos difíciles, alza tu mirada y recuerda que "
     "Dios es fiel."),

    # 41–60: Fuego y pasión por Dios
    ("🔥 'No se apagará el fuego del altar.' — Levítico 6:13\n"
     "Cuida ese fuego interior que Dios ha encendido en ti."),

    ("El fuego de Dios no es para ser consumido, sino para arder "
     "y transformar tu vida."),

    ("No permitas que el cansancio apague tu pasión por Dios; "
     "busca avivarla cada día."),

    ("La oración, la Palabra y la comunión son la leña que mantiene "
     "vivo el fuego."),

    ("'Sé ferviente en espíritu.' — Romanos 12:11\nNo dejes que tu fe "
     "se enfríe, sé constante y entusiasta."),

    ("La verdadera pasión por Dios se refleja en tu servicio y amor "
     "al prójimo."),

    ("No esperes sentir para actuar; la obediencia aviva el fuego "
     "en tu corazón."),

    ("El fuego que arde en ti es señal de vida, transformación "
     "y propósito."),

    ("Si sientes la llama baja, busca a Dios con más ganas; "
     "Él nunca falla."),

    ("Un corazón ardiente es un corazón rendido y obediente "
     "a Dios."),

    ("El Espíritu Santo enciende en ti un fuego que no puede "
     "apagarse."),

    ("Mantén tu fe encendida alimentándola con la Palabra "
     "y la adoración."),

    ("No dejes que las distracciones del mundo enfríen tu pasión "
     "espiritual."),

    ("El fuego de Dios purifica y sana. Deja que arda en ti "
     "sin miedo."),

    ("La pasión por Dios es contagiosa; enciende a otros con "
     "tu fe viva."),

    ("El fuego en el altar de tu vida atrae la presencia y el poder "
     "de Dios."),

    ("No reprimas el fuego que Dios puso en ti; déjalo brillar "
     "con valentía."),

    ("La fe sin pasión es fría. Busca un avivamiento diario "
     "en tu espíritu."),

    ("Que tu vida sea un altar donde nunca se apague el fuego "
     "de Dios."),

    "¡Reaviva tu fe hoy y arde para el Señor!",

    # 61–80: Perseverancia y prueba
    ("🏆 'Bienaventurado el que persevera bajo la prueba.' — "
     "Santiago 1:12\nCada prueba fortalece tu fe. No te rindas."),

    ("Dios usa la dificultad para moldear un carácter aprobado "
     "y fuerte."),

    ("La corona de vida es para los que aman a Dios y perseveran "
     "hasta el fin."),

    ("Las pruebas no son castigos, sino oportunidades para crecer "
     "en Él."),

    ("En la prueba, confía que Dios está contigo y tiene "
     "un propósito."),

    ("No corras cuando llegan las dificultades; camina firme "
     "con fe."),

    ("La perseverancia en la fe es más valiosa que cualquier "
     "éxito temporal."),

    ("Cuando sientas ganas de rendirte, recuerda la promesa de la "
     "corona de vida."),

    "Las dificultades son temporales; la recompensa es eterna.",

    ("Cada paso en la prueba es un paso más cerca de la "
     "bendición."),

    ("La paciencia en la prueba produce esperanza que no "
     "decepciona."),

    "Mantente firme y no pierdas de vista el amor de Dios.",

    "En la adversidad, tu fe se muestra genuina y fuerte.",

    "La prueba revela tu verdadero corazón y lo purifica.",

    ("Confía que Dios usará tu prueba para testimonio y "
     "bendición."),

    ("No temas la prueba; teme alejarte de Dios en medio "
     "de ella."),

    "En la prueba, ora con más fe y recibe su fortaleza.",

    ("Perseverar es amar a Dios incluso cuando no entiendes "
     "el camino."),

    "En la batalla, Dios es tu escudo y tu victoria segura.",

    ("Recuerda: la corona de vida espera a los que permanecen "
     "fieles."),

    # 81–100: Oración y comunión con Dios
    ("🙏 La oración es el aliento del alma. ¿Con qué frecuencia "
     "respiras oración?"),

    "Orar no cambia a Dios, cambia tu corazón para ver Su poder.",

    "La comunión diaria con Dios fortalece tu espíritu y te guía.",

    "Cuando sientas debilidad, habla con Dios. Él escucha siempre.",

    ("La oración sincera abre puertas que ninguna fuerza "
     "puede cerrar."),

    ("No subestimes el poder de una palabra de fe dicha "
     "en oración."),

    ("La relación con Dios se cultiva en el silencio y la "
     "escucha atenta."),

    ("En la oración encuentra paz, dirección y renovada "
     "esperanza."),

    "La constancia en la oración es muestra de fe verdadera.",

    "Orar es reconocer que sin Dios no podemos nada.",

    "Abre tu corazón en oración, no escondas nada de Dios.",

    ("Orar con gratitud cambia tu perspectiva y renueva "
     "tu alma."),

    ("El poder de la oración mueve montañas y transforma "
     "vidas."),

    "Cuando ores, cree que recibirás, porque Dios es fiel.",

    ("La oración es diálogo, no monólogo; escucha también "
     "su voz."),

    "No hay oración pequeña; cada palabra cuenta en el Reino.",

    "Orar en comunidad fortalece la fe y une corazones.",

    ("Jesús nos enseñó a orar con fe, humildad "
     "y persistencia."),

    ("¿Cuándo fue la última vez que oraste sin pedir nada, "
     "solo para agradecer?"),

    ("Hoy, haz de la oración tu primer refugio, no tu "
     "último recurso.")
]

# Mezclar la lista para aleatorizar el orden (opcional)
random.shuffle(tweets)

# Archivo para guardar el progreso
PROGRESS_FILE = "twitter_progress.json"


def cargar_progreso():
    """Carga el progreso desde el archivo JSON"""
    try:
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"ultimo_indice": 0, "tweets_publicados": []}


def guardar_progreso(indice, tweet_publicado):
    """Guarda el progreso en el archivo JSON"""
    try:
        progreso = cargar_progreso()
        progreso["ultimo_indice"] = indice
        progreso["tweets_publicados"].append({
            "indice": indice,
            "tweet": tweet_publicado[:50] + "...",
            "fecha": datetime.datetime.now().isoformat()
        })

        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(progreso, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ Error al guardar progreso: {e}")


def publicar_tweet_seguro(tweet, max_intentos=3):
    """Publica un tweet con manejo de errores robusto"""
    for intento in range(max_intentos):
        try:
            response = client.create_tweet(text=tweet)
            if response.data:
                tweet_id = response.data['id']
                return True, f"Tweet publicado con ID: {tweet_id}"
        except tweepy.TooManyRequests:
            wait_time = (intento + 1) * 15 * 60  # 15, 30, 45 minutos
            wait_min = wait_time // 60
            print(f"⏳ Rate limit alcanzado. Esperando {wait_min} min...")
            time.sleep(wait_time)
        except tweepy.Forbidden as e:
            return False, f"Error de permisos: {e}"
        except tweepy.BadRequest as e:
            return False, f"Tweet inválido: {e}"
        except Exception as e:
            print(f"⚠️ Error en intento {intento + 1}: {e}")
            if intento < max_intentos - 1:
                time.sleep(60)  # Esperar 1 minuto antes del siguiente intento

    return False, "Falló después de todos los intentos"


def mostrar_estado_actual():
    """Muestra el estado actual del progreso"""
    progreso = cargar_progreso()
    total_tweets = len(tweets)
    publicados = progreso["ultimo_indice"]

    print("\n📊 Estado actual:")
    print(f"   Total de tweets: {total_tweets}")
    print(f"   Tweets publicados: {publicados}")
    print(f"   Tweets restantes: {total_tweets - publicados}")
    print(f"   Progreso: {(publicados/total_tweets)*100:.1f}%")

    if progreso["tweets_publicados"]:
        ultimo = progreso["tweets_publicados"][-1]
        print(f"   Último tweet: {ultimo['tweet']}")
        print(f"   Fecha: {ultimo['fecha']}")


def publicar_lote(cantidad=1, intervalo_minutos=15):
    """Publica una cantidad específica de tweets con intervalo"""
    progreso = cargar_progreso()
    inicio = progreso["ultimo_indice"]
    total_tweets = len(tweets)

    if inicio >= total_tweets:
        print("🎉 ¡Todos los tweets ya han sido publicados!")
        return

    fin = min(inicio + cantidad, total_tweets)
    print(f"\n🚀 Publicando tweets del {inicio + 1} al {fin}...")

    for i in range(inicio, fin):
        tweet = tweets[i]
        print(f"\n📝 Tweet {i + 1}/{total_tweets}")
        print(f"Contenido: {tweet[:80]}...")

        exito, mensaje = publicar_tweet_seguro(tweet)

        if exito:
            print(f"✅ {mensaje}")
            guardar_progreso(i + 1, tweet)
        else:
            print(f"❌ Error: {mensaje}")
            print("⚠️ Deteniendo publicación debido al error")
            break

        # Esperar entre tweets (excepto el último)
        if i < fin - 1:
            mins = intervalo_minutos
            print(f"⏳ Esperando {mins} min hasta el siguiente tweet...")
            time.sleep(intervalo_minutos * 60)

    mostrar_estado_actual()


def calcular_intervalo_mensual():
    """Calcula el intervalo en minutos para que los tweets duren un mes"""
    total_tweets = len(tweets)
    dias_mes = 30
    minutos_por_dia = 24 * 60
    minutos_mes = dias_mes * minutos_por_dia
    
    # Calcular intervalo en minutos
    intervalo_minutos = minutos_mes // total_tweets
    
    print("📊 Cálculo de programación:")
    print(f"   Total de tweets: {total_tweets}")
    print(f"   Duración objetivo: {dias_mes} días")
    horas = intervalo_minutos / 60
    print(f"   Intervalo: {intervalo_minutos} min ({horas:.1f} h)")
    
    return intervalo_minutos


def publicar_todos_los_tweets():
    """Publica todos los tweets automáticamente con intervalo calculado"""
    progreso = cargar_progreso()
    inicio = progreso["ultimo_indice"]
    total_tweets = len(tweets)
    
    if inicio >= total_tweets:
        print("🎉 ¡Todos los tweets ya han sido publicados!")
        return
    
    # Calcular intervalo para durar un mes
    intervalo_minutos = calcular_intervalo_mensual()
    
    print("\n🚀 Iniciando publicación automática...")
    print(f"📅 Comenzando desde el tweet {inicio + 1}")
    print(f"⏰ Intervalo: {intervalo_minutos} minutos entre tweets")
    print(f"🏁 Tweets restantes: {total_tweets - inicio}")
    
    for i in range(inicio, total_tweets):
        tweet = tweets[i]
        
        # Mostrar información del tweet actual
        print(f"\n📝 Tweet {i + 1}/{total_tweets}")
        print(f"📄 Contenido: {tweet[:100]}...")
        
        # Intentar publicar el tweet
        exito, mensaje = publicar_tweet_seguro(tweet)
        
        if exito:
            print(f"✅ {mensaje}")
            guardar_progreso(i + 1, tweet)
            
            # Mostrar progreso
            progreso_pct = ((i + 1) / total_tweets) * 100
            print(f"📈 Progreso: {progreso_pct:.1f}%")
            
        else:
            print(f"❌ Error: {mensaje}")
            print("⚠️ Deteniendo publicación debido al error")
            break
        
        # Esperar antes del siguiente tweet (excepto si es el último)
        if i < total_tweets - 1:
            ahora = datetime.datetime.now()
            delta = datetime.timedelta(minutes=intervalo_minutos)
            siguiente_hora = ahora + delta
            formato_hora = siguiente_hora.strftime('%Y-%m-%d %H:%M:%S')
            print(f"⏳ Próximo tweet programado para: {formato_hora}")
            print(f"💤 Esperando {intervalo_minutos} minutos...")
            
            try:
                time.sleep(intervalo_minutos * 60)
            except KeyboardInterrupt:
                print("\n⚠️ Publicación interrumpida por el usuario")
                print(f"📍 Progreso guardado en tweet {i + 1}")
                break
    
    print("\n🎉 ¡Publicación automática completada!")
    mostrar_estado_actual()


def main():
    """Función principal del programa"""
    print("🐦 Bot de Twitter para Tweets Cristianos")
    print("=" * 50)
    
    try:
        mostrar_estado_actual()
        print("\n🤖 Modo automático activado")
        print("🔄 El script publicará todos los tweets automáticamente")
        print("⚡ Presiona Ctrl+C para detener en cualquier momento")
        
        # Pequeña pausa para que el usuario pueda leer
        time.sleep(3)
        
        # Iniciar publicación automática
        publicar_todos_los_tweets()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Operación interrumpida por el usuario")
        print("💾 El progreso se ha guardado automáticamente")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print("💾 El progreso se ha guardado automáticamente")


app = FastAPI()

@app.post("/publicar")
def publicar_endpoint(background_tasks: BackgroundTasks):
    """Endpoint para iniciar la publicación automática de tweets en segundo plano"""
    background_tasks.add_task(main)
    return {"status": "ok", "message": "Publicación iniciada en segundo plano"}

if __name__ == "__main__":
    # Ejecutar como API web en el puerto definido por la variable de entorno PORT o 8000 por defecto
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("publicar_tuits:app", host="0.0.0.0", port=port, reload=False)