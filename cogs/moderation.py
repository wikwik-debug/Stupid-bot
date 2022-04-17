import discord
from discord import TextChannel, User, Embed, Guild, PermissionOverwrite
from discord.ext import commands
import asyncio

class Moderation(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #The kick command
  @commands.command(case_insensitive = True)
  @commands.has_permissions(kick_members = True)
  async def kick(self, ctx, member : discord.Member, *, reason=None):
    if reason is None:
      await ctx.reply("Please provide a reason")
    else:
      try:
        kickEmbed = Embed(
          description = f"You have been kicked from ``{ctx.guild.name}``\nReason: {reason}",
          color = 0xff0000
        )
        
        await member.send(embed = kickEmbed)
      except:
        await ctx.send("cant send a DM to the user")
        print("cant send a DM to the user")

      await member.kick(reason=reason)
      await ctx.message.add_reaction("<a:ApprovedCheckBox:882777440609521724>")

  #The ban command
  @commands.command()
  @commands.has_permissions(ban_members = True)
  async def ban(self, ctx, member : commands.MemberConverter, *, reason=None):
    await member.ban(reason=reason)
    await ctx.message.add_reaction("<a:ApprovedCheckBox:882777440609521724>")

  #The unban command
  @commands.command()
  @commands.has_permissions(ban_members = True)
  async def unban(self, ctx, user: User):
    bannedUser = await self.bot.fetch_user(user.id)
    await ctx.guild.unban(bannedUser)
    await ctx.message.add_reaction("<a:ApprovedCheckBox:882777440609521724>")
  
  #The clear command
  @commands.command()
  @commands.has_permissions(manage_messages = True)
  async def clear(self, ctx, amount: int):
    
    await ctx.channel.purge(limit = amount)
  
  #The nickname command
  @commands.command(pass_content=False, aliases = ["changeNick"])
  @commands.has_permissions(manage_nicknames = True)
  async def nickname(self, ctx, member: discord.Member, *, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')
  
  class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
      amount = argument[:-1]
      unit = argument[-1]

      if amount.isdigit() and unit in ["h", "m", "s"]:
        return (int(amount), unit)

  #The mute command
  @commands.command()
  @commands.has_permissions(manage_messages = True)
  async def mute(self, ctx, member:discord.Member, duration: DurationConverter, reason = None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    guild = ctx.guild


    if role not in guild.roles:
      perms = discord.Permissions(send_messages=False, speak=False)
      
      await guild.create_role(name="Muted", permissions=perms)
        
      multiplier = {"d": 86400, "h": 3600, "m": 60, "s": 1}
      amount, unit = duration 

      await member.add_roles(role)

      embed = Embed(
        description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been muted for {amount}{unit}",
        color = 0x44b582
      )

      await ctx.send(embed = embed)
      
      await asyncio.sleep(amount * multiplier[unit])
      
      await member.remove_roles(role)
    
    elif reason is None:
      await ctx.message.add_reaction("<a:DeniedBox:882782174208749608>") 
    
    else:
      multiplier = {"d": 86400, "h": 3600, "m": 60, "s": 1}
      amount, unit = duration 
        
      await member.add_roles(role)
          
      embed2 = Embed(
        description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been muted for {amount}{unit}",
        color = 0x44b582
      )
      
      await ctx.send(embed = embed2)
      
      await asyncio.sleep(amount * multiplier[unit])
      
      await member.remove_roles(role)


  #The unmute command
  @commands.command()
  @commands.has_permissions(manage_messages = True)
  async def unmute(self, ctx, member : discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    
    await member.remove_roles(role)

    embed3 = Embed(
          description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been unmuted",
          color = 0x44b582
        )

    await ctx.send(embed = embed3)
  
  #The slowmode command
  @commands.command()
  @commands.has_permissions(manage_channels = True)
  async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f'The slowmode have been set to ``{seconds}`` seconds')
  
  #The lock commmand
  @commands.command()
  @commands.has_permissions(manage_channels = True)
  async def lock(self, ctx, channelName: TextChannel = None):
    channel = ctx.channel if channelName is None else await self.bot.fetch_channel(channelName.id)

    defaultRole = ctx.guild.default_role
    
    overwrite = PermissionOverwrite()
    
    overwrite.send_messages = False
    overwrite.use_slash_commands = False

    await channel.set_permissions(defaultRole, overwrite=overwrite)

    await ctx.send(f"{channel.mention} have been successfully locked")
    
  
  #The unlock command
  @commands.command()
  @commands.has_permissions(manage_channels = True)
  async def unlock(self, ctx, channelName: TextChannel = None):

    channel = ctx.channel if channelName is None else await self.bot.fetch_channel(channelName.id)
    
    defaultRole = ctx.guild.default_role

    overwrite = PermissionOverwrite()
    
    overwrite.send_messages = True
    
    await channel.set_permissions(defaultRole, overwrite=overwrite)
    
    
    await ctx.send(f"{channel.mention} have been successfully unlocked")
  
  #The channelban command
  @commands.command(aliases = ["cb"])
  @commands.has_permissions(ban_members = True)
  async def channelban(self, ctx, member: discord.Member, reason = None):
    
    overwrite = PermissionOverwrite()
    
    overwrite.view_channel = False
    
    if reason is None:
      return await ctx.reply("Please provide a reason")
    
    await ctx.channel.set_permissions(member, overwrite=overwrite)
    
    await ctx.send(f"{member.mention} have been banned from this channel")
  
  @commands.command()
  async def random(self, ctx):
    colour = discord.Colour
    
    randomEmbed = Embed(
      title = "random",
      description = "This is random",
      color = colour.random()
    )
    
    await ctx.send(embed = randomEmbed)
  
  #the globalkick command (for the owners only)
  @commands.command()
  async def globalkick(self, ctx, guild: Guild, user: User, *, reason = None):
    fetchedGuild = await self.bot.fetch_guild(guild.id)
    appinfo = await self.bot.application_info()
    
    if reason is None:
      await ctx.reply("Please provide a reason to kick")
    elif ctx.author != appinfo.owner:
      await ctx.reply("You cant execute this command because your not the owner of the bot")
    else:
      await fetchedGuild.kick(user, reason=reason)
      await ctx.send(f"Successfully kicked {user.mention} from `{guild.name}`")




def setup(bot):
  bot.add_cog(Moderation(bot))