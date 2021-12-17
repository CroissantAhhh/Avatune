from os import environ, name
# from werkzeug.security import generate_password_hash
from app.models import db, User, Medium, Artist, Album, Track, Playlist, PlaylistLink, UserTrackPlays
import datetime as dt
from random import randint, choice, sample
import string
from seeds.media_data import media_data
from seeds.album_data import albums_data
import json

def generate_hash_id():
    return ''.join(choice(string.ascii_letters + string.digits) for _ in range(20))

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
            hashed_id = generate_hash_id(),
            title = medium_data["name"],
            media_image = medium_data["bannerURL"],
            info_link = medium_data["infoLink"],
            description = medium_data["description"]
        )
        db.session.add(new_medium)
    db.session.commit()

def seed_artists():
    '''
    Seeds the artists table.
    '''
    yuki_hayashi = Artist(
        hashed_id = generate_hash_id(),
        name = 'Yuki Hayashi',
        artist_image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639761880/yuki_hayashi_upv6xo.jpg",
        bio = "Yuki Hayashi was born in Kyoto, Japan 1980. A former male rhythmic gymnast, selecting music as a performer led him to the world of accompaniment music. Although he had no formal musical training, he started composing music on his own while in university. After graduating he learned the basics of track making from Hideo Kobayashi, and began to produce accompaniment music for competitive dance in earnest. His unique musical style came about from his experience as a former dance, having taken in music from various genres, as well as his particular attention to a sense of unity between the music and the images."
    )
    db.session.add(yuki_hayashi)

    masafumi_takada = Artist(
        hashed_id = generate_hash_id(),
        name = 'Masafumi Takada',
        artist_image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639762741/Masafumi_Takada_uezvdl.jpg",
        bio = "Masafumi Takada is a japanese video game music composer. He is well known for his versatility in music with styles ranging from rock, pop, ballad, techno and jazz. He started learning music at the age of three on a keyboard called the Electrone by Yamaha. He then took the tuba in a brass band in high school. Takada joined the video game industry after obtaining his degree in music and worked on his first game called 2Tax Gold. His most notable work is the soundtrack composition for Grasshopper Manufacture games such as Killer7 and No More Heroes. He often partners up with musician and guitarist Jun Fukuda. He left Grasshopper in 2010 to join Shinji Mikami (creator of Resident Evil)'s company called Tango Gameworks. Takada has also composed soundtracks for God Hand, Resident Evil: The Umbrella Chronicles, Super Smash Bros. Brawl and beatmania IIDX. He left Grasshopper sometime in 2010 and is now working with Shinji Mikami's company Tango Gameworks. He also founded his own company called Sound Prestige. His favorite own soundtrack is Killer7."
    )
    db.session.add(masafumi_takada)

    takeru_kanazaki = Artist(
        hashed_id = generate_hash_id(),
        name = 'Takeru Kanazaki',
        artist_image = 'https://res.cloudinary.com/dmtj0amo0/image/upload/v1639763152/Takeru_Kanazaki_ufngku.jpg',
        bio = 'Takeru Kanazaki is a video game composer at Intelligent Systems. He has worked mainly on games of the WarioWare and Fire Emblem franchises. Fellow composer Hiroki Morishita and him are commonly referred to as the "Cavalier Duo", with Kanazaki being the green cavalier.'
    )
    db.session.add(takeru_kanazaki)

    hiroki_morishita = Artist(
        hashed_id = generate_hash_id(),
        name = 'Hiroki Morishita',
        artist_image = 'https://res.cloudinary.com/dmtj0amo0/image/upload/v1639763433/Hiroki_Morishita_gx3nx3.jpg',
        bio = 'Hiroki Morishita (JP) is an Intelligent Systems composer. He has been the main composer of the Fire Emblem series since New Mystery of the Emblem. Fellow composer Takeru Kanazaki and him are commonly referred to as the "Cavalier Duo", with Morishita being the red cavalier.'
    )
    db.session.add(hiroki_morishita)

    rei_kondoh = Artist(
        hashed_id = generate_hash_id(),
        name = 'Rei Kondoh',
        artist_image = 'https://res.cloudinary.com/dmtj0amo0/image/upload/v1639763532/Rei_Kondoh_iq9x7l.jpg',
        bio = "Rei Kondoh is a prolific composer and sound designer at T's Music. He has worked on several video games through his career, including various games on the Bayonetta, Fire Emblem, and Mario Party franchises. He has also composed music for TV series and cinema, as well as some original CDs of his own work."
    )
    db.session.add(rei_kondoh)

    masakazu_sugimori = Artist(
        hashed_id = generate_hash_id(),
        name = 'Masakazu Sugimori',
        artist_image = 'https://res.cloudinary.com/dmtj0amo0/image/upload/v1639765652/masakazu_sugimori_xuxwwn.jpg',
        bio = "Masakazu Sugimori (杉森 雅和 Sugimori Masakazu) is a video game composer who worked on the soundtrack for Phoenix Wright: Ace Attorney and Phoenix Wright: Ace Attorney: Justice For All, as well as providing the voice of Manfred von Karma in the Japanese versions of the games. Sugimori's other works include the soundtrack for Ghost Trick: Phantom Detective.",
    )
    db.session.add(masakazu_sugimori)

    noriyuki_iwadare = Artist(
        hashed_id = generate_hash_id(),
        name = 'Noriyuki Iwadare',
        artist_image = 'https://res.cloudinary.com/dmtj0amo0/image/upload/v1639766321/2560px-Noriyuki_Iwadare_20100701_Japan_Expo_43_rhdmlp.jpg',
        bio = "Iwadare was born in Matsumoto City, Nagano Prefecture, Japan. He began to compose video game music after years of being involved with university bands. The first award he won the Best Game Music award, the Mega Drive/Genesis category for Lunar: The Silver Star in 1991. He also won the Best Game Music award in the Sega Saturn Music category for Grandia in 1997 and in the Dreamcast category for Grandia 2 in 2000. Iwadare first composed music for Tokyo Disney Resort, in addition to Japanese dance programs, television programs, and radio programs. He dreams to have orchestral arrangements of his musical works, while he himself has done several times, as with the Gyakuten Meets Orchestra arrangements (orchestral arrangements of the Ace Attorney series music)."
    )
    db.session.add(noriyuki_iwadare)

    minako_adachi = Artist(
        hashed_id = generate_hash_id(),
        name = 'Minako Adachi',
        artist_image = 'https://res.cloudinary.com/dmtj0amo0/image/upload/v1639766580/Minako_Adachi_ctn3zy.jpg',
        bio = "Minako Adachi (Japanese: 足立美奈子 Adachi Minako) is a video game composer. She worked on various games on the company Pure Sound until she joined Game Freak during the development of Pokémon Black and White, games for which she also designed the sound effects. She has been involved in the soundtrack of the core series games ever since, as well as Game Freak's HarmoKnight. Her work is featured in Pokémon Black & Pokémon White: Super Music Collection, Pokémon Black 2 & Pokémon White 2: Super Music Collection, Pokémon X & Pokémon Y: Super Music Collection, and Pokémon Omega Ruby & Pokémon Alpha Sapphire: Super Music Collection."
    )
    db.session.add(minako_adachi)

    go_ichinose = Artist(
        hashed_id = generate_hash_id(),
        name = 'Go Ichinose',
        artist_image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639766697/3639-1480781694_kccekp.png",
        bio = "Gō Ichinose (Japanese: 一之瀬剛) is a Japanese video game composer best known for his work on the Pokémon series. Ichinose joined Game Freak since he wanted to acquire some career qualifications. At first, he worked there as a programmer and planner, but he soon worked full-time on composition. Junichi Masuda brought him to help with the soundtrack of Pokémon Gold and Silver. He has been credited as a composer in all of the core series games up to Pokémon Black 2 and White 2. He has also composed for other Game Freak titles such as Drill Dozer and Pocket Card Jockey. Ichinose also worked on sound effects on Pokémon FireRed and LeafGreen and Pokémon Emerald, and designed the Pokémon cries of Pokémon Diamond and Pearl, Pokémon Platinum, Pokémon HeartGold and SoulSilver, Pokémon Black and White, and Pokémon Black 2 and White 2. After Pokémon Black 2 and White 2, Gō Ichinose took a break from Pokémon to work on Pocket Card Jockey. He returned in Pokémon Sun and Moon."
    )
    db.session.add(go_ichinose)

    junichi_masuda = Artist(
        hashed_id = generate_hash_id(),
        name = 'Junichi Masuda',
        artist_image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639766890/Junichi_Masuda_yvmbkg.jpg",
        bio = "Junichi Masuda (増田 順一, Masuda Jun'ichi, born January 12, 1968) is a Japanese video game composer, director, designer, producer, singer, programmer and trombonist, best known for his work in the Pokémon franchise. He is a member of the Game Freak board of directors, and has been employed at the company since 1989 when he founded it alongside Satoshi Tajiri and Ken Sugimori. With the development of new Pokémon games, Masuda took new roles in future projects. He began to produce and direct games, starting with Pokémon Ruby and Sapphire, and became responsible for approving new character models. His style seeks to keep games accessible while still adding increasing levels of complexity. His work sticks to older mainstays of the series, including a focus on handheld game consoles and 2D graphics. His music draws inspiration from the work of celebrated modern composers like Dmitri Shostakovich, though he used the Super Mario series as a model of good video game composition."
    )
    db.session.add(junichi_masuda)

    akihiko_narita = Artist(
        hashed_id = generate_hash_id(),
        name = 'Akihiko Narita',
        artist_image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639767280/akihiko_narita_fcallh.png",
        bio = "Akihiko Narita is a Japanese video game composer. He is employed by Capcom. Narita is notable for working on a few games from the Monster Hunter franchise and Resident Evil 5. He recently led the music team of Resident Evil 6."
    )
    db.session.add(akihiko_narita)

    yuko_komiyama = Artist(
        hashed_id = generate_hash_id(),
        name = "Yuko Komiyama",
        artist_image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639767760/yuko_komiyama_ookctx.jpg",
        bio = "Yuko Komiyama is a Japanese sound composer who composed various titles for the Mega Man X series. In 2010, Komiyama left the Capcom and founded comymusic, where she works freelance. In 2013, she joined sound production company Unique Note.",
    )
    db.session.add(yuko_komiyama)

    capcom_sound_team = Artist(
        hashed_id = generate_hash_id(),
        name = "Capcom Sound Team",
        artist_image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639771889/capcomsoundteam_ejxvcg.jpg",
        bio = "Capcom's Sound Team"
    )
    db.session.add(capcom_sound_team)

    toshio_masuda = Artist(
        hashed_id = generate_hash_id(),
        name = "Toshio Masuda",
        artist_image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639772122/A-2906439-1537631953-5910.jpeg_jyllf0.jpg",
        bio = "Toshio Masuda (増田 俊郎, Masuda Toshio, born October 28, 1959) is a Japanese composer. He has composed and synthesized scores for several Japanese television shows and animated series. Masuda is perhaps best known as the composer of the 2002 hit anime series Naruto where he combined traditional instruments like the shamisen and shakuhachi together with guitar, drums, bass, piano and other keyboard instruments along with chanting."
    )
    db.session.add(toshio_masuda)

    yasuharu_takanashi = Artist(
        hashed_id = generate_hash_id(),
        name = "Yasuharu Takanashi",
        artist_image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639772292/yasuharu_takanashi_ypdodo.jpg",
        bio = "Yasuharu Takanashi (高梨 康治, Takanashi Yasuharu, born April 13, 1963) is a prolific Japanese composer and arranger for anime and video game series. His anime composition credits include Beyblade G-Revolution, Hell Girl, Ikki Tousen, Naruto Shippuden, Fairy Tail, Shiki, and Sailor Moon Crystal. He also composed on four Pretty Cure series: Fresh Pretty Cure!, HeartCatch PreCure!, Suite PreCure, and Smile PreCure!, as well as their related films, some of which were with composer Naoki Sato. Game music compositions include Genji: Dawn of the Samurai, Genji: Days of the Blade and J-Stars Victory VS. He also composed theme music for Pride Fighting Championships and Ultraman Max.",
    )
    db.session.add(yasuharu_takanashi)

    db.session.commit()

def seed_albums():
    for album_data in albums_data:
        new_album = Album(
            hashed_id = generate_hash_id(),
            title = album_data["name"],
            album_image = album_data["albumImageURL"],
            medium_id = int(album_data["mediumId"])
        )
        db.session.add(new_album)
        album_artists = album_data["artist"].split("/")
        for album_artist in album_artists:
            artist_instance = Artist.query.filter(Artist.name == album_artist).one()
            new_album.album_artists.append(artist_instance)
            artist_instance.artist_albums.append(new_album)
    db.session.commit()

def seed_tracks():
    pass
