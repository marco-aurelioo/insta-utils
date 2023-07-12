import requests
import instaloader
import subprocess


def download_instagram_media(username):
    loader = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        i = 0
        # Baixar imagens individuais
        for post in profile.get_posts():
            i = i+1
            filename: str = "marcia_amorimcake"+str(i)+".jpg"
            if not post.is_video:
                loader.download_pic( filename, post.url, post.date_utc)

        # Baixar álbuns de imagens
        for post in profile.get_posts():
            if post.is_album:
                loader.download_album(post, f'{post.date_utc.strftime("%Y%m%d_%H%M%S")}/')

        # Baixar histórias
        loader.download_stories([profile.userid], profile.username)

        print("Download concluído!")
    except instaloader.exceptions.ProfileNotExistsException:
        print("O perfil não existe.")
    except instaloader.exceptions.InstaloaderException:
        print("Erro ao fazer o download da mídia.")



def download_instagram_videos(username, target_directory):
    loader = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(loader.context, username)

        # Baixar vídeos
        for post in profile.get_posts():
            if post.is_video:
                video_url = post.video_url
                filename = f'{post.date_utc.strftime("%Y%m%d_%H%M%S")}.mp4'
                target_path = f'{target_directory}/{filename}'
                download_video_from_url(video_url, target_path)

                # Converter o formato do vídeo
                #convert_to_mp4(target_path)

        print("Download e conversão concluídos!")
    except instaloader.exceptions.ProfileNotExistsException:
        print("O perfil não existe.")
    except instaloader.exceptions.InstaloaderException:
        print("Erro ao fazer o download dos vídeos.")

def download_video_from_url(url, target_path):
    response = requests.get(url, True)
    response.raise_for_status()
    with open(target_path, 'wb') as file:
        for chunk in response.iter_content(8192):
            file.write(chunk)

#def convert_to_mp4(video_path):
#    output_path = video_path.replace('.mp4', '_converted.mp4')
#    subprocess.run(['ffmpeg', '-i', video_path, '-c:v', 'libx264', '-preset', 'slow', '-crf', '23', '-c:a', 'copy', output_path])



def download_instagram_images(username):
    loader = instaloader.Instaloader()

    try:
        # Fazer o download das imagens do perfil
        loader.download_profile(username, False)
        print("Download concluído!")
    except instaloader.exceptions.ProfileNotExistsException:
        print("O perfil não existe.")

# Definir o diretório de destino dos vídeos
target_directory = './videos'
# Chamar a função de download
download_instagram_videos('perfil', target_directory)
#download_instagram_media('profile')