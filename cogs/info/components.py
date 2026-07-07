from disnake import ActivityType, Colour, CustomActivity, MediaGalleryItem, Member, SeparatorSpacing, User
from disnake.activity import Activity, Game, Spotify, Streaming
from disnake.enums import Status
from disnake.ext.commands import Bot
from disnake.ui import Button, Container, MediaGallery, Section, Separator, TextDisplay, Thumbnail
from disnake.utils import format_dt, get
from core.utils import escape


async def activities_components(member: Member):
    components = []

    for activity in member.activities:
        if activity.type == ActivityType.unknown: continue
        container = []

        if isinstance(activity, Activity):
            status = activity.type.name.title()
            if activity.type == ActivityType.listening:
                status += ' to'
            details = activity.details
            state = activity.state
            title = activity.name or ''

            name = escape(f'{status} {title}') if details else escape(status)
            details = f'**{escape(details)}**' if details else f'**{escape(title)}**'
            state = escape(state) if state else None
            timestamp = format_dt(t, 'R') if (t := activity.start or activity.end) else None

            text = TextDisplay('\n'.join(line for line in (name, details, state, timestamp) if line))
            if activity.large_image_url:
                container.append(Section(text, accessory=Thumbnail(activity.large_image_url)))
            else:
                container.append(text)

        elif isinstance(activity, Game):
            text = TextDisplay(f'**{activity.name}**')
            if activity.large_image_url:
                container.append(Section(text, accessory=Thumbnail(activity.large_image_url)))
            else:
                container.append(text)

        elif isinstance(activity, Streaming):
            text = TextDisplay(f'Streaming\n**{activity.name}**\n{activity.details}')
            if activity.large_image_url:
                container.append(Section(text, accessory=Thumbnail(activity.large_image_url)))
            else:
                container.append(text)

        elif isinstance(activity, Spotify):
            timestamp = format_dt(t, 'R') if (t := activity.start or activity.end) else None
            text = TextDisplay(f'Listening to Spotify\n**{activity.title}**\n{activity.artist}\n{timestamp}')
            if activity.album_cover_url:
                container.append(Section(text, accessory=Thumbnail(activity.album_cover_url)))
            else:
                container.append(text)

        if container:
            components.append(Container(*container))

    return components


async def member_components(bot: Bot, user: User, member: Member):
    emojis = await bot.fetch_application_emojis()

    is_streaming = member.activity and member.activity.type == ActivityType.streaming
    is_mobile = member.status == Status.online and member.is_on_mobile()
    status_emoji = get(emojis, name='streaming' if is_streaming else 'mobile' if is_mobile else member.status.name)
    status = f'{status_emoji or ''} {escape(member.status.name)}'
    activity = ' '.join(str(i) for i in (member.activity.emoji, member.activity.name) if i) if isinstance(member.activity, CustomActivity) else None
    displayed_roles = [role.mention for role in member.roles if role.hoist]
    username = f'{member.name}#{member.discriminator}' if member.bot else member.name

    container = []
    header = f'# {escape(member.display_name)}' + (f' {member.role_icon}' if member.role_icon else '')
    text = [f'{member.mention} {status}']
    if activity:
        text.extend([
            f'### Status',
            f'> {escape(activity)}'
        ])
    text.extend([
        f'### Member since / Created at',
        f'> {format_dt(member.joined_at) if member.joined_at else '`Unknown`'} / {format_dt(member.created_at)}',
    ])
    footer = [
        escape(username),
        str(member.id),
        f'[Avatar url]({member.display_avatar.url})'
    ]

    if displayed_roles:
        text.extend([
            f'### Displayed roles',
            f'>>> {'\n'.join(reversed(displayed_roles[-10:]))}'
        ])

    if member.bot:
        container.extend([
            Section(header, accessory=Button(label='BOT', disabled=True)),
            TextDisplay('\n'.join(text))
        ])
    elif decoration := member.display_avatar_decoration:
        container.append(Section(header, '\n'.join(text), accessory=Thumbnail(decoration)))
        footer.append(f'[Decoration url]({decoration.url})')
    else:
        container.extend([
            TextDisplay(header),
            TextDisplay('\n'.join(text))
        ])

    container.append(Separator(spacing=SeparatorSpacing.large))

    if banner := (member.guild_banner or user.banner):
        container.append(MediaGallery(MediaGalleryItem(banner)))
        footer.append(f'[Banner url]({banner.url})')

    container.extend([
        MediaGallery(MediaGalleryItem(member.display_avatar)),
        TextDisplay('-# ' + ' ・ '.join(footer))
    ])

    activities = await activities_components(member)

    return [
        Container(*container, accent_colour=member.colour if member.colour != Colour(0) else None),
        *activities[:9]
    ]


async def user_components(_: Bot, user: User):
    username = f'{user.name}#{user.discriminator}' if user.bot else user.name

    container = []
    header = f'# {escape(user.display_name)}'
    text = [
        f'### {user.mention}',
        f'### Created at',
        f'> {format_dt(user.created_at)}',
    ]
    footer = [
        escape(username),
        str(user.id),
        f'[Avatar url]({user.display_avatar.url})'
    ]

    if user.bot:
        container.extend([
            Section(header, accessory=Button(label='BOT', disabled=True)),
            TextDisplay('\n'.join(text))
        ])
    elif decoration := user.avatar_decoration:
        container.append(Section(header, '\n'.join(text), accessory=Thumbnail(decoration)))
        footer.append(f'[Decoration url]({decoration.url})')
    else:
        container.extend([
            TextDisplay(header),
            TextDisplay('\n'.join(text))
        ])

    container.append(Separator(spacing=SeparatorSpacing.large))

    if user.banner:
        container.append(MediaGallery(MediaGalleryItem(user.banner)))
        footer.append(f'[Banner url]({user.banner.url})')

    container.extend([
        MediaGallery(MediaGalleryItem(user.display_avatar)),
        TextDisplay('-# ' + ' ・ '.join(footer))
    ])

    return Container(*container, accent_colour=user.accent_colour if user.accent_colour != Colour(0) else None),
