# -*- coding:utf8 -*-

# インストールした discord.py を読み込む
import discord
# 自分のBotのアクセストークンをconfig.pyに書いておく
# config.pyは同じディレクトリ内に配置
import config
import requests
# pythonでパスワード付きzipを作成するモジュール
import pyminizip
import os

# -----------------------------------クラス分けしたほうがいい------------------------------------
# ファイルをダウンロードする関数
# import requests
def download(title, url):
    try:
        r = requests.get(url)
        # openの中で保存先のパス（ファイル名を指定）
        with open("添付ファイルの保存先のディレクトリのパス" + title, mode='w') as f:
            f.write(r.text)
    except requests.exceptions.RequestException as err:
        print(err)
# --------------------------------------------------------------------------------

# 自分のBotのアクセストークンをconfig.pyに書いておく
TOKEN = config.TOKEN

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # ファイルを添付して、「/zip」が含まれていたらローカルに保存
    # テキストに「/zip」が含まれているか判定
    if "/zip" in message.content.split():
        text = message.content.split()
        # ifで分岐 パスワード入力があるかどうか
        try:
            password = text[1]

            # 投稿されたファイルの詳細を取得
            file = message.attachments[0]
            # ファイルを保存
            download(file.filename, file.url)
            await message.channel.send("パスワード付き" + file.filename + ".zipを返します")

            # 保存したファイルをパスワード付きzipに変換
            # IndexError: list index out of range
            pyminizip.compress("添付ファイルを保存したディレクトリのパス" + file.filename,"/","zipファイルを保存したいディレクトリのパス" + file.filename + ".zip",password,9)

            # zipしたファイルを送り返す
            await message.channel.send(file=discord.File("zipファイルを保存したディレクトリのパス" + file.filename + ".zip"))
            # ファイルの削除
            # 権限をbotに与えないと使えないエラー発生
            # discord.errors.Forbidden: 403 Forbidden (error code: 50013): Missing Permissions
            await message.delete()

            # 保存したファイルを削除
            os.remove("zipファイルを保存したディレクトリのパス" + file.filename + ".zip")
            os.remove("添付したファイルを保存したディレクトリのパス" + file.filename)

        # パスワード入力がなかった場合エラー
        except IndexError:
            await message.channel.send('パスワードを入力してください')


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
