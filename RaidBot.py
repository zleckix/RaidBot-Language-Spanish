import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
@commands.has_permissions(administrator=True)
async def spam(ctx, cantidad: int, *, mensaje: str):
    if cantidad > 1000:
        await ctx.send("Hay un máximo de `1,000` mensajes por canal para evitar bloqueos.")
        return

    tareas = []

    for canal in ctx.guild.text_channels:
        async def enviar_en_canal(canal):
            for _ in range(cantidad):
                try:
                    await canal.send(mensaje)
                    await asyncio.sleep(0)
                except discord.Forbidden:
                    print(f"No tengo permisos para enviar en {canal.name}")
                except Exception as e:
                    print(f"Error en {canal.name}: {e}")

        tareas.append(asyncio.create_task(enviar_en_canal(canal)))

    await asyncio.gather(*tareas)
    await ctx.send(f"Listo, mensaje enviado `{cantidad}` veces en todos los canales de texto.")

@bot.command()
@commands.has_permissions(administrator=True)
async def raid(ctx, cantidad: int, *, nombre_base: str):
    if cantidad > 500:
        await ctx.send("Hay un máximo de `500` canales por comando para evitar bloqueos.")
        return

    creados = 0
    for i in range(1, cantidad + 1):
        nombre = f"{nombre_base}-{i}"
        try:
            await ctx.guild.create_text_channel(name=nombre)
            creados += 1
        except discord.Forbidden:
            await ctx.send(f"No tengo permisos para crear canales.")
            return
        except Exception as e:
            await ctx.send(f"Error al crear `{nombre}`: {e}")

    await ctx.send(f"Listo, se han creado `{creados}` canales con el nombre {nombre_base}.")



@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    await ctx.send("Confirma que quieres borrar **TODOS LOS CANALES** del servidor escribiendo `y` en el chat.")

    def check(m):
        return m.author == ctx.author and m.content == "y"

    try:
        respuesta = await bot.wait_for('message', check=check, timeout=15)
        for canal in ctx.guild.channels:
            try:
                await canal.delete()
            except discord.Forbidden:
                print(f"No tengo permisos para borrar {canal.name}")
            except Exception as e:
                print(f"Error al borrar {canal.name}: {e}")
        await ctx.send("Listo, todos los canales han sido borrados.")
    except asyncio.TimeoutError:
        await ctx.send("Tiempo agotado. No se borró nada.")

@bot.command()
@commands.has_permissions(administrator=True)
async def cn(ctx, *, nuevo_nombre: str):
    try:
        await ctx.guild.edit(name=nuevo_nombre)
        await ctx.send(f"El nombre del servidor ha sido cambiado a: `{nuevo_nombre}`")
    except discord.Forbidden:
        await ctx.send("No tengo permisos para cambiar el nombre del servidor.")
    except Exception as e:
        await ctx.send(f"Error al cambiar el nombre: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def ci(ctx):
    if not ctx.message.attachments:
        await ctx.send("Debes adjuntar una imagen para usar como nuevo icono.")
        return

    imagen = ctx.message.attachments[0]
    try:
        imagen_bytes = await imagen.read()
        await ctx.guild.edit(icon=imagen_bytes)
        await ctx.send("Icono del servidor cambiado correctamente.")
    except discord.Forbidden:
        await ctx.send("No tengo permisos para cambiar el icono del servidor.")
    except Exception as e:
        await ctx.send(f"Error al cambiar el icono: {e}")
        
@bot.command()
@commands.has_permissions(manage_roles=True)
async def cr(ctx, cantidad: int, *, nombre_base: str):
    if cantidad > 100:
        await ctx.send("Hay un máximo de `100` roles por comando para evitar bloqueos.")
        return

    creados = 0
    for i in range(1, cantidad + 1):
        nombre = f"{nombre_base}-{i}"
        try:
            await ctx.guild.create_role(name=nombre)
            creados += 1
            await asyncio.sleep(0.5)
        except discord.Forbidden:
            await ctx.send(f"No tengo permisos para crear el rol `{nombre}`.")
        except Exception as e:
            await ctx.send(f"Error al crear `{nombre}`: {e}")

    await ctx.send(f"Listo, se han creado `{creados}` roles con nombre base `{nombre_base}`.")

@bot.command()
@commands.has_permissions(administrator=True)
async def ping(ctx):
    try:
        latencia = round(bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Ping del bot: `{latencia}ms`")
    except discord.Forbidden:
        await ctx.send("No tengo permisos para enviar mensajes aquí.")
    except Exception as e:
        await ctx.send(f"Error al ejecutar el comando: {e}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def ret(ctx, cantidad: int, nombre_base: str, *, mensaje: str):
    if cantidad > 500:
        await ctx.send("Hay un máximo de `500` canales por comando para evitar bloqueos.")
        return

    creados = 0
    for i in range(1, cantidad + 1):
        nombre = f"{nombre_base}-{i}"
        try:
            canal = await ctx.guild.create_text_channel(name=nombre)
            await canal.send(mensaje)
            creados += 1
            await asyncio.sleep(0)
        except Exception as e:
            await ctx.send(f"Error en `{nombre}`: {e}")

    await ctx.send(f"Listo, se han creado `{creados}` canales y enviado el mensaje en cada uno.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def bn(ctx):
    miembros = ctx.guild.members
    miembros_que_no_se_banean = [ctx.author, ctx.guild.owner, bot.user]

    miembros_a_banear = [
        miembro for miembro in miembros
        if miembro not in miembros_que_no_se_banean and not miembro.bot
    ]

    baneados = 0
    for usuario in miembros_a_banear:
        try:
            await ctx.guild.ban(usuario, reason="Chuyin Bot.")
            baneados += 1
            await asyncio.sleep(1)
        except discord.Forbidden:
            await ctx.send(f"No tengo permisos para banear a `{usuario}`.")
        except Exception as e:
            await ctx.send(f"Error al banear `{usuario}`: {e}")

    await ctx.send(f"Listo, se han baneado `{baneados}` Personas.")

@bot.command()
@commands.has_permissions(administrator=True)
async def resetserer(ctx):
    await ctx.send(
        "Este comando eliminará **todos los canales** del servidor y los recreará vacíos.\n"
        "Escribe `confirmar` para continuar."
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "confirmar"

    try:
        await bot.wait_for("message", check=check, timeout=20)
    except asyncio.TimeoutError:
        await ctx.send("Tiempo agotado. Cancelado.")
        return

    await ctx.send("Reiniciando todos los canales...")

    canales_originales = list(ctx.guild.channels)

    for canal in canales_originales:
        try:
            nuevo = await canal.clone()
            await canal.delete()
            await nuevo.edit(name=canal.name, category=canal.category, position=canal.position)
            await asyncio.sleep(1.5)
        except Exception as e:
            await ctx.send(f"Error al reiniciar canal `{canal.name}`: {e}")

    await ctx.send("Todos los canales han sido reiniciados.")

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx):
    try:
        await ctx.send("Borrando todos los mensajes del canal...")
        await ctx.channel.purge(limit=None)
        confirmacion = await ctx.send("Todos los mensajes han sido borrados.")
        await asyncio.sleep(5)
        await confirmacion.delete()
    except discord.Forbidden:
        await ctx.send("No tengo permisos para borrar mensajes.")
    except Exception as e:
        await ctx.send(f"Error al borrar mensajes: {e}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def resetcanal(ctx):
    canal = ctx.channel
    nombre = canal.name
    categoria = canal.category

    await ctx.send(f"Este comando eliminará el canal `{nombre}` y lo recreará vacío.\nEscribe `y` para continuar.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "y"

    try:
        await bot.wait_for("message", check=check, timeout=15)
    except asyncio.TimeoutError:
        await ctx.send("Tiempo agotado. Cancelado.")
        return

    try:
        nuevo = await canal.clone()
        await canal.delete()
        await nuevo.edit(name=nombre, category=categoria)
        await nuevo.send(f"Canal `{nombre}` ha sido reiniciado.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name="hlp")
async def hlp(ctx):
    embed = discord.Embed(
        title="Comandos de el RaidBot",
        description="Aquí están los comandos disponibles:",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Canal",
        value="`$clearall` – Borra todos los mensajes de un solo canal\n`$resetcanal` – resetea un canal borrando todos los mensajes enviados en el pero conservando la configuración de roles y el nombre de el canal.\n`$resetserver` – resetea TODOS los canales del servidor borrando todos los mensajes enviados en el pero conservando la configuración de roles y el nombre de el canal.",
        inline=False
    )

    embed.add_field(
        name="ℹ️ Raid Info",
        value="`$spam <cantidad> <mensaje>` – Hace spam en todos los canales.\n`$raid <Cantidad de canales a crear> <Nombre de los canales>` – Crea una cantidad personalizada de canales.\n`$nuke` – Borra todos los canales del servidor.\n`$cn <Nuevo nombre del servidor>` – Crea un nuevo nombre al servidor.\n`$cr <cantidad> <nombre de los roles>` – Crea una cantidad de roles en el servidor.\n`$ci <Adjunta una imagen>` – Crea una nueva foto para el servidor.\n`$ret <Cantidad> <Nombre de canales a crear> <Mensaje de Spam>` – Raidea el servidor creando una cantidad absurda de canales con un nombre y mensaje de spam personalizado.\n`$bn` – Banea a todos los miembros del servidor excepto a los bots con administrador.",
        inline=False
    )

    embed.add_field(
        name="ℹ️ Ayuda",
        value="`$hlp` – Muestra este panel de ayuda de comandos\n`$ping` – Mostrar la latencia del bot\n - ***Recuerda que el bot debe ser activado por su creador***.",
        inline=False
    )

    embed.set_footer(text="Bot de Raideo")
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

bot.run("TU TOKEN AQUI")
