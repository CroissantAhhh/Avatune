from os import environ, name
from werkzeug.security import generate_password_hash
from app.models import db, User, Medium, Artist, Album, Track, Playlist, PlaylistLink, UserTrackPlays
import datetime as dt
from random import randint, choice, sample
from seeds.media_data import media_data
from seeds.album_data import album_data
import json

def seed_users():
    '''
    Seeds the users table.
    '''
    jason = User(
        username='Jason Zhou', email='jasonzhou8597@gmail.com', password='jasonzhou2')

    db.session.add(jason)

    db.session.commit()


def seed_media():
    '''
    Seeds the media table.
    '''
    for medium_data in media_data:
        new_medium = Medium(
            title = medium_data.name,
            media_image = medium_data.bannerURL,
            info_link = medium_data.infoLink,
            description = medium_data.description
        )
        db.session.add(new_medium)
    db.session.commit()

def seed_artists():
    '''
    Seeds the artists table.
    '''
    yuki_hayashi = Artist(
        name = 'Yuki Hayashi',
        artist_image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639761880/yuki_hayashi_upv6xo.jpg",
        bio = "Yuki Hayashi was born in Kyoto, Japan 1980. A former male rhythmic gymnast, selecting music as a performer led him to the world of accompaniment music. Although he had no formal musical training, he started composing music on his own while in university. After graduating he learned the basics of track making from Hideo Kobayashi, and began to produce accompaniment music for competitive dance in earnest. His unique musical style came about from his experience as a former dance, having taken in music from various genres, as well as his particular attention to a sense of unity between the music and the images."
    )
    db.session.add(yuki_hayashi)

    masafumi_takada = Artist(
        name = 'Masafumi Takada',
        artist_image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639762741/Masafumi_Takada_uezvdl.jpg",
        bio = "Masafumi Takada is a japanese video game music composer. He is well known for his versatility in music with styles ranging from rock, pop, ballad, techno and jazz. He started learning music at the age of three on a keyboard called the Electrone by Yamaha. He then took the tuba in a brass band in high school. Takada joined the video game industry after obtaining his degree in music and worked on his first game called 2Tax Gold. His most notable work is the soundtrack composition for Grasshopper Manufacture games such as Killer7 and No More Heroes. He often partners up with musician and guitarist Jun Fukuda. He left Grasshopper in 2010 to join Shinji Mikami (creator of Resident Evil)'s company called Tango Gameworks. Takada has also composed soundtracks for God Hand, Resident Evil: The Umbrella Chronicles, Super Smash Bros. Brawl and beatmania IIDX. He left Grasshopper sometime in 2010 and is now working with Shinji Mikami's company Tango Gameworks. He also founded his own company called Sound Prestige. His favorite own soundtrack is Killer7."
    )
    db.session.add(masafumi_takada)

    takeru_kanazaki = Artist(
        name = 'Takeru Kanazaki',
        artist_image = 'https://res.cloudinary.com/dmtj0amo0/image/upload/v1639763152/Takeru_Kanazaki_ufngku.jpg',
        bio = 'Takeru Kanazaki is a video game composer at Intelligent Systems. He has worked mainly on games of the WarioWare and Fire Emblem franchises. Fellow composer Hiroki Morishita and him are commonly referred to as the "Cavalier Duo", with Kanazaki being the green cavalier.'
    )
    db.session.add(takeru_kanazaki)

    hiroki_morishita = Artist(
        name = 'Hiroki Morishita',
        artist_image = 'https://res.cloudinary.com/dmtj0amo0/image/upload/v1639763433/Hiroki_Morishita_gx3nx3.jpg',
        bio = 'Hiroki Morishita (JP) is an Intelligent Systems composer. He has been the main composer of the Fire Emblem series since New Mystery of the Emblem. Fellow composer Takeru Kanazaki and him are commonly referred to as the "Cavalier Duo", with Morishita being the red cavalier.'
    )
    db.session.add(hiroki_morishita)

    rei_kondoh = Artist(
        name = 'Rei Kondoh',
        artist_image = 'https://res.cloudinary.com/dmtj0amo0/image/upload/v1639763532/Rei_Kondoh_iq9x7l.jpg',
        bio = "Rei Kondoh is a prolific composer and sound designer at T's Music. He has worked on several video games through his career, including various games on the Bayonetta, Fire Emblem, and Mario Party franchises. He has also composed music for TV series and cinema, as well as some original CDs of his own work."
    )
    db.session.add(rei_kondoh)
