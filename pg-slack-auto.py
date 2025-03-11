from sshtunnel import SSHTunnelForwarder
import psycopg2
import pandas as pd
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging

# ログ設定（例：~/logs/script.logに出力）
logging.basicConfig(
    filename="/<YOUR_DIRECTORY_PATH>>/script.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

logging.info("スクリプト実行開始")

# SSHトンネルの設定
with SSHTunnelForwarder(
    ('<YOUR_EC2_IP>', 22),
    ssh_username="<YOUR_EC2_USER>",           # 例: "ec2-user" または "ubuntu"
    ssh_pkey="/<YOUR_DIRECTORY_PATH>>/id_ed25519",                # 秘密鍵のパス (例: "~/.ssh/id_ed25519")
    ssh_private_key_password="<YOUR_PASS_PHRASE>",
    remote_bind_address=('localhost', 5432)  # PostgreSQLが稼働しているホストとポート
) as tunnel:
    # PostgreSQLに接続
    conn = psycopg2.connect(
        database="<YOUR_PG_DATABASE>",
        user="<YOUR_PG_USER>",
        password="<YOUR_PG_PASSWORD>",
        host='localhost',                    # ローカルホスト経由で接続
        port=tunnel.local_bind_port          # トンネルで転送されたローカルポート
    )
    
    # SQLクエリの実行と結果のDataFrameへの取り込み
    query = """
        <YOUR_PG_SQL>
    """
    df = pd.read_sql_query(query, conn)
    
    # 接続を閉じる
    conn.close()
    
    # Excelファイルとしてローカルに保存
    df.to_excel("/<YOUR_DIRECTORY_PATH>>/output.xlsx", index=False)
    logging.info("Excelファイルの作成が完了しました。")

    if not df.empty:
        # Slackに送信
        df_text = df.to_string(index=False)

        # Slack Botトークンと送信先チャネル
        slack_token = "<YOUR_SLACK_Bot User OAuth Token>>"  # 取得したBotトークンに置き換え
        channel = "#<YOUR_SLACK_CHANNEL>"  # 送信したいチャネル名（例: "#general"）

        client = WebClient(token=slack_token)
        try:
            response = client.chat_postMessage(
                channel=channel,
                text=f"<@<YOUR_SLACK_ID>>\n```{df_text}```"  # 特定のユーザーにメンションにて通知を行っている
            )
            logging.info("Slackに通知を送信しました。")
        except SlackApiError as e:
            logging.error(f"Slack通知エラー: {e.response['error']}")
    else:
        logging.info("SQL結果が空のため、Slack通知は行いません。")


logging.info("スクリプト実行終了")
