from os import environ, name
from werkzeug.security import generate_password_hash
from app.models import db, User, Medium, Artist, Album, Track, Playlist, PlaylistLink, UserTrackPlays, Follow
import datetime as dt
from random import randint, choice, sample
import string
from pathlib import Path
import json

media_data = [
    { "name": "Haikyu!!", "bannerURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1640213637/Haikyu%21%21/haikyucover_pf1lv4.jpg", "infoLink": "https://myanimelist.net/anime/20583/Haikyuu", "description": "Haikyu!! is a Japanese manga series written and illustrated by Haruichi Furudate. The story follows Shōyō Hinata, a boy determined to become a great volleyball player despite his small stature." },
    { "name": "My Hero Academia", "bannerURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1633810874/My%20Hero%20Academia/MHABanner_xjn34b.jpg", "infoLink": "https://myanimelist.net/anime/31964/Boku_no_Hero_Academia", "description": "My Hero Academia is a Japanese superhero manga series written and illustrated by Kōhei Horikoshi. The story follows Izuku Midoriya, a boy born without superpowers in a world where they have become commonplace, but who still dreams of becoming a superhero himself."},
    { "name": "Fire Emblem", "bannerURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1640213608/Fire%20Emblem:%20Three%20Houses/fecover_dh63vy.jpg", "infoLink": "https://www.nintendo.com/games/detail/fire-emblem-three-houses-switch/", "description": "Fire Emblem: Three Houses is a tactical role-playing game developed by Intelligent Systems and Koei Tecmo for the Nintendo Switch and published worldwide by Nintendo."},
    { "name": "Danganronpa", "bannerURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1640213537/Danganronpa/danganronpacover_g1zedi.jpg", "infoLink": "http://danganronpa.us/", "description": "Danganronpa is a Japanese video game franchise created by Kazutaka Kodaka and developed and owned by Spike Chunsoft. The series surrounds a group of high school students who are forced into murdering each other by a bear named Monokuma. Gameplay features a mix of adventure, visual novel, and dating simulator elements."},
    { "name": "Ace Attorney", "bannerURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634658328/Ace%20Attorney/Box_Front_ex2mua.jpg", "infoLink": "https://www.ace-attorney.com/", "description": "Ace Attorney is a series of adventure video game legal dramas developed by Capcom. The first entry in the series, Phoenix Wright: Ace Attorney, was released in 2001; since then, five further main series games, as well as various spin-offs and high-definition remasters for newer game consoles, have been released." },
    { "name": "Pokemon", "bannerURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634839074/Pokemon/pokemonBanner_vartur.jpg", "infoLink": "https://www.pokemon.com/us/", "description": "An anime series based on the popular Game Boy game 'Pocket Monsters' in which children raise a pocket monster and train it to fight other monsters. In this show, Satoshi and his Pokemon, Pikachu, travel the land hoping to improve their skills and eventually become the grand champions."},
    { "name": "Monster Hunter", "bannerURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1635108408/Monster%20Hunter/Screen_Shot_2021-10-24_at_1.46.21_PM_l9ce6g.png", "infoLink": "https://www.monsterhunter.com/", "description": "The games are primarily action role-playing games. The player takes the role of a Hunter, slaying or trapping large monsters across various landscapes as part of quests given to them by locals, with some quests involving the gathering of a certain item or items, which may put the Hunter at risk of facing various monsters. As part of its core gameplay loop, players use loot gained from slaying monsters, gathering resources, and quest rewards to craft improved weapons, armor, and other items that allow them to face more powerful monsters. All main series titles feature multiplayer (usually up to four players cooperatively), but can also be played single player."},
    { "name": "Naruto", "bannerURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1635872773/Naruto/narutoImage_hqtsiu.jpg", "infoLink": "https://myanimelist.net/anime/20/Naruto", "description": "Naruto is a Japanese manga series written and illustrated by Masashi Kishimoto. It tells the story of Naruto Uzumaki, a young ninja who seeks recognition from his peers and dreams of becoming the Hokage, the leader of his village." },
]

albums_data = [
      { "name": "Haikyu!! Original Soundtrack Vol.1", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1633811079/Haikyu%21%21/Original%20Soundtrack%20Vol%201/Cover_pjjinj.jpg", "artist": "Yuki Hayashi", "mediumId": 1},
      { "name": "Haikyu!! Original Soundtrack Vol.2", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1633811363/Haikyu%21%21/Original%20Soundtrack%20Vol%202/cover_at9bjm.jpg", "artist": "Yuki Hayashi", "mediumId": 1},
      { "name": "Haikyu!! Second Season Original Soundtrack Vol.1", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1633811914/Haikyu%21%21/Second%20Season%20Original%20Soundtrack%20Vol%201/img262_isp1cn.jpg", "artist": "Yuki Hayashi", "mediumId": 1},
      { "name": "Haikyu!! Second Season Original Soundtrack Vol.2", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1633814944/Haikyu%21%21/Second%20Season%20Original%20Soundtrack%20Vol%202/h2s2_zpkfn2.jpg", "artist": "Yuki Hayashi", "mediumId": 1},
      { "name": "My Hero Academia Original Soundtrack", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1633812164/My%20Hero%20Academia/Season%201%20Soundtrack/Cover_eum1j5.jpg", "artist": "Yuki Hayashi", "mediumId": 2},
      { "name": "My Hero Academia 2nd Original Soundtrack", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1633812748/My%20Hero%20Academia/Season%202%20Soundtrack/Cover_uftllj.jpg", "artist": "Yuki Hayashi", "mediumId": 2},
      { "name": "Fire Emblem Three Houses Complete Soundtrack", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1633817292/Fire%20Emblem:%20Three%20Houses/Cover_edf4kd.jpg", "artist": "Takeru Kanazaki/Hiroki Morishita/Rei Kondoh", "mediumId": 3},
      { "name": "Danganronpa Trigger Happy Havoc Original Soundtrack", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1633813259/Danganronpa/Trigger%20Happy%20Havoc/Cover_lzzx4r.jpg", "artist": "Masafumi Takada", "mediumId": 4},
      { "name": "Haikyu!! Karasuno High School VS Shiratorizawa Academy Original Soundtrack", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634656717/Haikyu%21%21/Karasuno%20vs%20Shiratorizawa%20OST/Cover_mhbrex.jpg", "artist": "Yuki Hayashi", "mediumId": 1},
      { "name": "Haikyu!! To The Top Original Soundtrack", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634657108/Haikyu%21%21/To%20the%20Top%21%20OST/Cover_egrsmg.jpg", "artist": "Yuki Hayashi", "mediumId": 1},
      { "name": "Phoenix Wright: Ace Attorney Original Soundtrack", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634657896/Ace%20Attorney/Game%201/Disc_1_Front_vtn3d7.jpg", "artist": "Masakazu Sugimori", "mediumId": 5},
      { "name": "Phoenix Wright: Ace Attorney - Justice for All - Original Soundtrack", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634658075/Ace%20Attorney/Game%202/Disc_2_Front_cva0lf.jpg", "artist": "Masakazu Sugimori", "mediumId": 5},
      { "name": "Phoenix Wright: Ace Attorney - Trials and Tribulations - Original Soundtrack", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634658320/Ace%20Attorney/Game%203/Disc_3_Front_sqefry.jpg", "artist": "Noriyuki Iwadare", "mediumId": 5},
      { "name": "My Hero Academia 3rd Original Soundtrack", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634660757/My%20Hero%20Academia/Season%203%20Soundtrack/Cover_hk04uo.jpg", "artist": "Yuki Hayashi", "mediumId": 2},
      { "name": "My Hero Academia 4th Original Soundtrack", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634661090/My%20Hero%20Academia/Season%204%20Soundtrack/Cover_ja9etg.jpg", "artist": "Yuki Hayashi", "mediumId": 2},
      { "name": "My Hero Academia 5th Original Soundtrack", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634838338/My%20Hero%20Academia/Season%205%20Soundtrack/cover_w907yk.jpg", "artist": "Yuki Hayashi", "mediumId": 2},
      { "name": "Pokemon Sword & Pokemon Shield: Super Music Collection", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634663647/Pokemon/Sword-Shield/Cover_y525tr.png", "artist": "Minako Adachi/Go Ichinose", "mediumId": 6},
      { "name": "Pokemon Diamond & Pokemon Pearl: Super Music Collection", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634662995/Pokemon/Diamond-Pearl/Cover_ddhg7n.png", "artist": "Junichi Masuda/Go Ichinose", "mediumId": 6},
      { "name": "Monster Hunter: World Original Soundtrack", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634664624/Monster%20Hunter/Monster%20Hunter%20World/Cover_sqkabe.png", "artist": "Akihiko Narita/Yuko Komiyama", "mediumId": 7},
      { "name": "Monster Hunter World: Iceborne Original Soundtrack", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634666012/Monster%20Hunter/Monster%20Hunter%20World%20-%20Iceborne/COVER_mpvmbk.jpg", "artist": "Akihiko Narita/Yuko Komiyama", "mediumId": 7},
      { "name": "Monster Hunter: Hunting Music Ultimate Collection", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1635285727/Monster%20Hunter/Hunting%20Music%20Ultimate%20Collection/Cover_q2a3ot.jpg", "artist": "Capcom Sound Team", "mediumId": 7},
      { "name": "Naruto Original Soundtrack", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634658424/Naruto/Naruto%201/Cover_nrtxl6.jpg", "artist": "Toshio Masuda", "mediumId": 8},
      { "name": "Naruto Original Soundtrack II", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634658748/Naruto/Naruto%202/Cover_qm9obd.jpg", "artist": "Toshio Masuda", "mediumId": 8},
      { "name": "Naruto Original Soundtrack III", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634658937/Naruto/Naruto%203/Cover_gbni3k.jpg", "artist": "Toshio Masuda", "mediumId": 8},
      { "name": "Naruto Shippuden: Original Soundtrack", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634659892/Naruto/Naruto%20Shippuden%201/Cover_ntwyb4.jpg", "artist": "Yasuharu Takanashi", "mediumId": 8},
      { "name": "Naruto Shippuden: Original Soundtrack II", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634660161/Naruto/Naruto%20Shippuden%202/Cover_wl6fnj.jpg", "artist": "Yasuharu Takanashi", "mediumId": 8},
      { "name": "Naruto Shippuden: Original Soundtrack III", "albumImageURL": "https://res.cloudinary.com/dmtj0amo0/image/upload/v1634660403/Naruto/Naruto%20Shippuden%203/Cover_k0qoum.jpg", "artist": "Yasuharu Takanashi", "mediumId": 8},
]

playlist_images = [
    'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/datetech.jpeg',
    'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/karasuno.jpeg',
    'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/seijoh.jpeg',
    'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/johzenji.jpeg',
    'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/wakunan.jpeg',
    'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/shiratorizawa.jpeg',
    'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/nekoma.jpeg',
    'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/fukurodani.jpeg',
    'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/inarizaki.jpeg',
    'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/tsubakihara.jpeg',
    'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/kamomedai.jpeg',
    'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/nohebi.jpeg',
    'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/itachiyama.jpeg'
]

def generate_hash_id():
    return ''.join(choice(string.ascii_letters + string.digits) for _ in range(20))

def seed_users():
    '''
    Seeds the users table.
    '''
    jason = User(
        hashed_id = generate_hash_id(),
        username = 'Jason Zhou',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/oikawa.png',
        email = 'jasonzhou8597@gmail.com',
        password = 'jasonzhou2',
    )

    db.session.add(jason)

    danp = User(
        hashed_id = generate_hash_id(),
        username = 'Dan Purcell',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/ukai.jpg',
        email = 'danp@gmail.com',
        password = 'password',
    )
    db.session.add(danp)

    michaele = User(
        hashed_id = generate_hash_id(),
        username = 'Michael Ericson',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/nishinoya.jpg',
        email = 'michaele@gmail.com',
        password = 'password',
    )
    db.session.add(michaele)

    nebyou = User(
        hashed_id = generate_hash_id(),
        username = 'Nebyou Ejigu',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/ojiro.jpeg',
        email = 'daemail@gmail.com',
        password = 'password',
    )
    db.session.add(nebyou)

    annd = User(
        hashed_id = generate_hash_id(),
        username = 'Ann Donnelly',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/mikachan.jpg',
        email = 'annd@gmail.com',
        password = 'password',
    )
    db.session.add(annd)

    jamest = User(
        hashed_id = generate_hash_id(),
        username = 'James Thompson',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/osamu.jpeg',
        email = 'jamest@gmail.com',
        password = 'password',
    )
    db.session.add(jamest)

    pstory = User(
        hashed_id = generate_hash_id(),
        username = 'Patrick Story',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/tanaka.jpeg',
        email = 'pstory@gmail.com',
        password = 'password',
    )
    db.session.add(pstory)

    willzill = User(
        hashed_id = generate_hash_id(),
        username = 'William Ziller',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/aone.jpeg',
        email = 'williamz@gmail.com',
        password = 'password',
    )
    db.session.add(willzill)

    samo = User(
        hashed_id = generate_hash_id(),
        username = 'Sam Ortega',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/sugawara.jpg',
        email = 'samo@gmail.com',
        password = 'password',
    )
    db.session.add(samo)

    garrettm = User(
        hashed_id = generate_hash_id(),
        username = 'Garrett Middleton',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/shinsuke.jpg',
        email = 'garrettm@gmail.com',
        password = 'password',
    )
    db.session.add(garrettm)

    ajabush = User(
        hashed_id = generate_hash_id(),
        username = 'AJ Abushaban',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/akaashi.jpg',
        email = 'ajabush@gmail.com',
        password = 'password',
    )
    db.session.add(ajabush)

    revan = User(
        hashed_id = generate_hash_id(),
        username = 'Revan Fajardo',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/atsumu.jpg',
        email = 'revanf@gmail.com',
        password = 'password',
    )
    db.session.add(revan)

    brandonl = User(
        hashed_id = generate_hash_id(),
        username = 'Brandon Laursen',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/suguru.jpeg',
        email = 'brandonl@gmail.com',
        password = 'password',
    )
    db.session.add(brandonl)

    nicks = User(
        hashed_id = generate_hash_id(),
        username = 'Nick Sim',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/terushima.jpg',
        email = 'nicks@gmail.com',
        password = 'password',
    )
    db.session.add(nicks)

    adamg = User(
        hashed_id = generate_hash_id(),
        username = 'Adam Guan',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/kenma.png',
        email = 'adamg@gmail.com',
        password = 'password',
    )
    db.session.add(adamg)

    kiaram = User(
        hashed_id = generate_hash_id(),
        username = 'Kiara Mendaros',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/yachi.jpg',
        email = 'kiaram@gmail.com',
        password = 'password',
    )
    db.session.add(kiaram)

    nevinc = User(
        hashed_id = generate_hash_id(),
        username = 'Nevin Chow',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/goshiki.jpeg',
        email = 'nevinc@gmail.com',
        password = 'password',
    )
    db.session.add(nevinc)

    jessiez = User(
        hashed_id = generate_hash_id(),
        username = 'Jessie Zhuo',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/yukie.png',
        email = 'jessiez@gmail.com',
        password = 'password',
    )
    db.session.add(jessiez)

    howardc = User(
        hashed_id = generate_hash_id(),
        username = 'Howard Chang',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/hinata.jpg',
        email = 'howardc@gmail.com',
        password = 'password',
    )
    db.session.add(howardc)

    davidr = User(
        hashed_id = generate_hash_id(),
        username = 'David Rogers',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/tsukishima.jpeg',
        email = 'davidr@gmail.com',
        password = 'password',
    )
    db.session.add(davidr)

    robk = User(
        hashed_id = generate_hash_id(),
        username = 'Rob Kauth',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/shirabu.jpeg',
        email = 'robk@gmail.com',
        password = 'password',
    )
    db.session.add(robk)

    brads = User(
        hashed_id = generate_hash_id(),
        username = 'Brad Simpson',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/kyotani.jpg',
        email = 'brads@gmail.com',
        password = 'password',
    )
    db.session.add(brads)

    ish_chaudry = User(
        hashed_id = generate_hash_id(),
        username = 'Ish Chaudry',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/tendou.jpg',
        email = 'ishc@gmail.com',
        password = 'password',
    )
    db.session.add(ish_chaudry)

    chrisw = User(
        hashed_id = generate_hash_id(),
        username = 'Chris Wu',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/ushijima.jpg',
        email = 'chrisw@gmail.com',
        password = 'password',
    )
    db.session.add(chrisw)

    dannyk = User(
        hashed_id = generate_hash_id(),
        username = 'Danny Kim',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/bokuto.jpg',
        email = 'dannyk@gmail.com',
        password = 'password'
    )
    db.session.add(dannyk)

    kwang = User(
        hashed_id = generate_hash_id(),
        username = 'Kwang Kim',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/kuroo.jpg',
        email = 'kwangk@gmail.com',
        password = 'password',
    )
    db.session.add(kwang)

    anish = User(
        hashed_id = generate_hash_id(),
        username = 'Anish Velagapudi',
        image = 'https://avatune-profile-pics.s3.us-west-2.amazonaws.com/kageyama.jpg',
        email = 'anishv@gmail.com',
        password = 'password'
    )
    db.session.add(anish)

    db.session.commit()
    for user1 in User.query.all():
        for user2 in User.query.all():
            if user1.id != user2.id:
                probability = randint(1, 100)
                if probability <= 40:
                    new_follow = Follow(
                        follower_id = user1.id,
                        followed_id = user2.id
                    )
                    db.session.add(new_follow)
                    db.session.commit()

def seed_media():
    '''
    Seeds the media table.
    '''
    for medium_data in media_data:
        new_medium = Medium(
            hashed_id = generate_hash_id(),
            title = medium_data["name"],
            image = medium_data["bannerURL"],
            info_link = medium_data["infoLink"],
            description = medium_data["description"]
        )
        db.session.add(new_medium)
        db.session.commit()
        print(User.query.all())
        for user in User.query.all():
            print(user.id)
            probability = randint(1, 100)
            if probability <= 50:
                user.user_media.append(new_medium)
                new_medium.medium_users.append(user)
                db.session.commit()
    db.session.commit()

def seed_artists():
    '''
    Seeds the artists table.
    '''
    yuki_hayashi = Artist(
        hashed_id = generate_hash_id(),
        title = 'Yuki Hayashi',
        image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639761880/yuki_hayashi_upv6xo.jpg",
        bio = "Yuki Hayashi was born in Kyoto, Japan 1980. A former male rhythmic gymnast, selecting music as a performer led him to the world of accompaniment music. Although he had no formal musical training, he started composing music on his own while in university. After graduating he learned the basics of track making from Hideo Kobayashi, and began to produce accompaniment music for competitive dance in earnest. His unique musical style came about from his experience as a former dance, having taken in music from various genres, as well as his particular attention to a sense of unity between the music and the images."
    )
    db.session.add(yuki_hayashi)
    db.session.commit()

    masafumi_takada = Artist(
        hashed_id = generate_hash_id(),
        title = 'Masafumi Takada',
        image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639762741/Masafumi_Takada_uezvdl.jpg",
        bio = "Masafumi Takada is a japanese video game music composer. He is well known for his versatility in music with styles ranging from rock, pop, ballad, techno and jazz. He started learning music at the age of three on a keyboard called the Electrone by Yamaha. He then took the tuba in a brass band in high school. Takada joined the video game industry after obtaining his degree in music and worked on his first game called 2Tax Gold. His most notable work is the soundtrack composition for Grasshopper Manufacture games such as Killer7 and No More Heroes."
    )
    db.session.add(masafumi_takada)
    db.session.commit()

    takeru_kanazaki = Artist(
        hashed_id = generate_hash_id(),
        title = 'Takeru Kanazaki',
        image = 'https://res.cloudinary.com/dmtj0amo0/image/upload/v1639763152/Takeru_Kanazaki_ufngku.jpg',
        bio = 'Takeru Kanazaki is a video game composer at Intelligent Systems. He has worked mainly on games of the WarioWare and Fire Emblem franchises. Fellow composer Hiroki Morishita and him are commonly referred to as the "Cavalier Duo", with Kanazaki being the green cavalier.'
    )
    db.session.add(takeru_kanazaki)

    hiroki_morishita = Artist(
        hashed_id = generate_hash_id(),
        title = 'Hiroki Morishita',
        image = 'https://res.cloudinary.com/dmtj0amo0/image/upload/v1639763433/Hiroki_Morishita_gx3nx3.jpg',
        bio = 'Hiroki Morishita (JP) is an Intelligent Systems composer. He has been the main composer of the Fire Emblem series since New Mystery of the Emblem. Fellow composer Takeru Kanazaki and him are commonly referred to as the "Cavalier Duo", with Morishita being the red cavalier.'
    )
    db.session.add(hiroki_morishita)

    rei_kondoh = Artist(
        hashed_id = generate_hash_id(),
        title = 'Rei Kondoh',
        image = 'https://res.cloudinary.com/dmtj0amo0/image/upload/v1639763532/Rei_Kondoh_iq9x7l.jpg',
        bio = "Rei Kondoh is a prolific composer and sound designer at T's Music. He has worked on several video games through his career, including various games on the Bayonetta, Fire Emblem, and Mario Party franchises. He has also composed music for TV series and cinema, as well as some original CDs of his own work."
    )
    db.session.add(rei_kondoh)

    masakazu_sugimori = Artist(
        hashed_id = generate_hash_id(),
        title = 'Masakazu Sugimori',
        image = 'https://res.cloudinary.com/dmtj0amo0/image/upload/v1639765652/masakazu_sugimori_xuxwwn.jpg',
        bio = "Masakazu Sugimori (杉森 雅和 Sugimori Masakazu) is a video game composer who worked on the soundtrack for Phoenix Wright: Ace Attorney and Phoenix Wright: Ace Attorney: Justice For All, as well as providing the voice of Manfred von Karma in the Japanese versions of the games. Sugimori's other works include the soundtrack for Ghost Trick: Phantom Detective.",
    )
    db.session.add(masakazu_sugimori)

    noriyuki_iwadare = Artist(
        hashed_id = generate_hash_id(),
        title = 'Noriyuki Iwadare',
        image = 'https://res.cloudinary.com/dmtj0amo0/image/upload/v1639766321/2560px-Noriyuki_Iwadare_20100701_Japan_Expo_43_rhdmlp.jpg',
        bio = "Iwadare was born in Matsumoto City, Nagano Prefecture, Japan. He began to compose video game music after years of being involved with university bands. The first award he won the Best Game Music award, the Mega Drive/Genesis category for Lunar: The Silver Star in 1991. He also won the Best Game Music award in the Sega Saturn Music category for Grandia in 1997 and in the Dreamcast category for Grandia 2 in 2000. Iwadare first composed music for Tokyo Disney Resort, in addition to Japanese dance programs, television programs, and radio programs. He dreams to have orchestral arrangements of his musical works, while he himself has done several times, as with the Gyakuten Meets Orchestra arrangements (orchestral arrangements of the Ace Attorney series music)."
    )
    db.session.add(noriyuki_iwadare)

    minako_adachi = Artist(
        hashed_id = generate_hash_id(),
        title = 'Minako Adachi',
        image = 'https://res.cloudinary.com/dmtj0amo0/image/upload/v1639766580/Minako_Adachi_ctn3zy.jpg',
        bio = "Minako Adachi (Japanese: 足立美奈子 Adachi Minako) is a video game composer. She worked on various games on the company Pure Sound until she joined Game Freak during the development of Pokémon Black and White, games for which she also designed the sound effects. She has been involved in the soundtrack of the core series games ever since, as well as Game Freak's HarmoKnight. Her work is featured in Pokémon Black & Pokémon White: Super Music Collection, Pokémon Black 2 & Pokémon White 2: Super Music Collection, Pokémon X & Pokémon Y: Super Music Collection, and Pokémon Omega Ruby & Pokémon Alpha Sapphire: Super Music Collection."
    )
    db.session.add(minako_adachi)

    go_ichinose = Artist(
        hashed_id = generate_hash_id(),
        title = 'Go Ichinose',
        image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639766697/3639-1480781694_kccekp.png",
        bio = "Gō Ichinose (Japanese: 一之瀬剛) is a Japanese video game composer best known for his work on the Pokémon series. Ichinose joined Game Freak since he wanted to acquire some career qualifications. At first, he worked there as a programmer and planner, but he soon worked full-time on composition. Junichi Masuda brought him to help with the soundtrack of Pokémon Gold and Silver. He has been credited as a composer in all of the core series games up to Pokémon Black 2 and White 2. He has also composed for other Game Freak titles such as Drill Dozer and Pocket Card Jockey. Ichinose also worked on sound effects on Pokémon FireRed and LeafGreen and Pokémon Emerald, and designed the Pokémon cries of Pokémon Diamond and Pearl, Pokémon Platinum, Pokémon HeartGold and SoulSilver, Pokémon Black and White, and Pokémon Black 2 and White 2. After Pokémon Black 2 and White 2, Gō Ichinose took a break from Pokémon to work on Pocket Card Jockey. He returned in Pokémon Sun and Moon."
    )
    db.session.add(go_ichinose)
    db.session.commit()

    junichi_masuda = Artist(
        hashed_id = generate_hash_id(),
        title = 'Junichi Masuda',
        image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639766890/Junichi_Masuda_yvmbkg.jpg",
        bio = "Junichi Masuda (増田 順一, Masuda Jun'ichi, born January 12, 1968) is a Japanese video game composer, director, designer, producer, singer, programmer and trombonist, best known for his work in the Pokémon franchise. He is a member of the Game Freak board of directors, and has been employed at the company since 1989 when he founded it alongside Satoshi Tajiri and Ken Sugimori. With the development of new Pokémon games, Masuda took new roles in future projects. He began to produce and direct games, starting with Pokémon Ruby and Sapphire, and became responsible for approving new character models. His style seeks to keep games accessible while still adding increasing levels of complexity. His work sticks to older mainstays of the series, including a focus on handheld game consoles and 2D graphics. His music draws inspiration from the work of celebrated modern composers like Dmitri Shostakovich, though he used the Super Mario series as a model of good video game composition."
    )
    db.session.add(junichi_masuda)

    akihiko_narita = Artist(
        hashed_id = generate_hash_id(),
        title = 'Akihiko Narita',
        image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639767280/akihiko_narita_fcallh.png",
        bio = "Akihiko Narita is a Japanese video game composer. He is employed by Capcom. Narita is notable for working on a few games from the Monster Hunter franchise and Resident Evil 5. He recently led the music team of Resident Evil 6."
    )
    db.session.add(akihiko_narita)

    yuko_komiyama = Artist(
        hashed_id = generate_hash_id(),
        title = "Yuko Komiyama",
        image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639767760/yuko_komiyama_ookctx.jpg",
        bio = "Yuko Komiyama is a Japanese sound composer who composed various titles for the Mega Man X series. In 2010, Komiyama left the Capcom and founded comymusic, where she works freelance. In 2013, she joined sound production company Unique Note.",
    )
    db.session.add(yuko_komiyama)

    capcom_sound_team = Artist(
        hashed_id = generate_hash_id(),
        title = "Capcom Sound Team",
        image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639771889/capcomsoundteam_ejxvcg.jpg",
        bio = "Capcom's Sound Team"
    )
    db.session.add(capcom_sound_team)

    toshio_masuda = Artist(
        hashed_id = generate_hash_id(),
        title = "Toshio Masuda",
        image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639772122/A-2906439-1537631953-5910.jpeg_jyllf0.jpg",
        bio = "Toshio Masuda (増田 俊郎, Masuda Toshio, born October 28, 1959) is a Japanese composer. He has composed and synthesized scores for several Japanese television shows and animated series. Masuda is perhaps best known as the composer of the 2002 hit anime series Naruto where he combined traditional instruments like the shamisen and shakuhachi together with guitar, drums, bass, piano and other keyboard instruments along with chanting."
    )
    db.session.add(toshio_masuda)
    db.session.commit()

    yasuharu_takanashi = Artist(
        hashed_id = generate_hash_id(),
        title = "Yasuharu Takanashi",
        image = "https://res.cloudinary.com/dmtj0amo0/image/upload/v1639772292/yasuharu_takanashi_ypdodo.jpg",
        bio = "Yasuharu Takanashi (高梨 康治, Takanashi Yasuharu, born April 13, 1963) is a prolific Japanese composer and arranger for anime and video game series. His anime composition credits include Beyblade G-Revolution, Hell Girl, Ikki Tousen, Naruto Shippuden, Fairy Tail, Shiki, and Sailor Moon Crystal. He also composed on four Pretty Cure series: Fresh Pretty Cure!, HeartCatch PreCure!, Suite PreCure, and Smile PreCure!, as well as their related films, some of which were with composer Naoki Sato. Game music compositions include Genji: Dawn of the Samurai, Genji: Days of the Blade and J-Stars Victory VS. He also composed theme music for Pride Fighting Championships and Ultraman Max.",
    )
    db.session.add(yasuharu_takanashi)
    db.session.commit()
    for artist in Artist.query.all():
        for user in User.query.all():
            probability = randint(1, 100)
            if probability <= 30:
                user.user_artists.append(artist)
                artist.artist_users.append(user)
                db.session.commit()

    db.session.commit()

def seed_albums():
    '''
    Seeds the albums table.
    '''
    for album_data in albums_data:
        new_album = Album(
            hashed_id = generate_hash_id(),
            title = album_data["name"],
            image = album_data["albumImageURL"],
            medium_id = int(album_data["mediumId"])
        )
        db.session.add(new_album)
        db.session.commit()
        album_artists = album_data["artist"].split("/")
        for album_artist in album_artists:
            artist_instance = Artist.query.filter(Artist.title == album_artist).one()
            new_album.album_artists.append(artist_instance)
            artist_instance.artist_albums.append(new_album)
            db.session.commit()

        for user in User.query.all():
            probability = randint(1, 100)
            if probability <= 30:
                user.user_albums.append(new_album)
                new_album.album_users.append(user)
                db.session.commit()
    db.session.commit()

def random_date():
    current_time = dt.datetime.now()
    seconds_random = randint(0, 32000000)
    return current_time - dt.timedelta(seconds=seconds_random)

def seed_tracks():
    '''
    Seeds the tracks table.
    '''
    paths = list(Path('app/seeds/trackData').glob('**/*.json'))
    for path in paths:
        with open(path) as json_file:
            tracks = json.load(json_file)
            for track in tracks:
                new_track = Track(
                    title = track["name"],
                    image = track["trackImageURL"],
                    track_file = track["fileURL"],
                    duration = 1000,
                    plays = randint(1000, 100000),
                    album_id = track["albumId"],
                    medium_id = track["mediumId"],
                )
                db.session.add(new_track)
                db.session.commit()

                track_album = Album.query.get(new_track.album_id)
                for album_artist in track_album.album_artists:
                    new_track.track_artists.append(album_artist)
                    album_artist.artist_tracks.append(new_track)
                    db.session.commit()

                db.session.commit()

def seed_playlists():
    '''
    Seeds the playlists table.
    '''
    words1 = ['chill', 'hardcore', 'epic', 'hip', 'emotional', 'lit', 'positive', 'sad']
    words2 = ['tunes', 'jams', 'bangers', 'vibes', 'songs', 'feelings', 'mix', 'classics', 'hits', 'mood']
    all_users = User.query.all()
    for user in all_users:
        yoursongs = Playlist(
            hashed_id = generate_hash_id(),
            title = 'Your Songs',
            user_id = user.id,
        )
        db.session.add(yoursongs)
        db.session.commit()
        for i in range(5):
            new_pl = Playlist(
                hashed_id = generate_hash_id(),
                title = f"{choice(words1)} {choice(words2)}",
                image = choice(playlist_images),
                user_id = user.id
            )
            db.session.add(new_pl)
        db.session.commit()
        user_playlists = [playlist.id for playlist in user.user_playlists]
        for track in Track.query.all():
            probability = randint(1, 100)
            if probability <= 30:
                new_pll = PlaylistLink(
                    track_id = track.id,
                    playlist_id = choice(user_playlists),
                    time_added = random_date(),
                )
                db.session.add(new_pll)
                db.session.commit()

    for user in all_users:
        for playlist in Playlist.query.all():
            if playlist.user_id != user.id and playlist.title != "Your Songs":
                probability = randint(1, 100)
                if probability <= 30:
                    playlist.playlist_following_users.append(user)
                    user.user_followed_playlists.append(playlist)
                    db.session.commit()
    db.session.commit()

def seed_utps():
    '''
    Seeds the usertrackplays table.
    '''
    for user in User.query.all():
        for track in Track.query.all():
            probability = randint(1, 100)
            if probability <= 30:
                new_utp = UserTrackPlays(
                    track_id = track.id,
                    user_id = user.id,
                    count = randint(0, 200),
                    last_played = random_date(),
                )
                db.session.add(new_utp)
                db.session.commit()
    db.session.commit()

def seed_all():
    '''
    Seeds all models.
    '''
    seed_users()
    seed_media()
    seed_artists()
    seed_albums()
    seed_tracks()
    seed_playlists()
    seed_utps()

def undo_all():
    '''
    Undos all seeded models.
    '''
    db.session.execute(f'TRUNCATE usertrackplays RESTART IDENTITY CASCADE;')
    db.session.execute(f'TRUNCATE playlists RESTART IDENTITY CASCADE;')
    db.session.execute(f'TRUNCATE tracks RESTART IDENTITY CASCADE;')
    db.session.execute(f'TRUNCATE albums RESTART IDENTITY CASCADE;')
    db.session.execute(f'TRUNCATE artists RESTART IDENTITY CASCADE;')
    db.session.execute(f'TRUNCATE media RESTART IDENTITY CASCADE;')
    db.session.execute(f'TRUNCATE users RESTART IDENTITY CASCADE;')
    db.session.commit()
