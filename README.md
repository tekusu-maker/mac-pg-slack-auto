# 🚀 mac-pg-slack-auto

## 🔗 メニュー
- [概要](#-概要)
- [SSH鍵の作成とAWS EC2への登録](#-1-ssh鍵の作成とaws-ec2への登録)
- [Slack APIの準備とアプリ作成](#-2-slack-apiの準備とアプリ作成)
- [Python環境のセットアップとライブラリのインストール](#-3-python環境のセットアップとライブラリのインストール)
- [launchctlによる自動実行の設定](#-4-launchctlによる自動実行の設定)

## 📝 概要
このリポジトリは、Pythonを用いてSSH接続を確立し、リモートのPostgreSQLデータベースから必要なデータを取得します。取得した情報をSlack APIを通じて通知することで、システムの監視や運用を効率化します。また、Mac上でlaunchdを利用して自動起動する設定も含まれており、定期実行環境を実現しています。

---

## 🔧 セットアップ手順

### 🛠 1. SSH鍵の作成とAWS EC2への登録
#### 🔹 SSH鍵の作成
   以下のコマンドでED25519形式のSSH鍵を生成します。
   ```sh
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
📌 **鍵の保存先:** `/Users/<YOUR_DIRECTORY_PATH>/.ssh/id_ed25519`

#### 🔹 AWS EC2への鍵登録
   AWSマネジメントコンソールにログインし、EC2の「Key Pairs」セクションに移動します。
   作成した公開鍵（id_ed25519.pub）をインポートし、EC2インスタンスで利用できるようにします。

---

### 💬 2. Slack APIの準備とアプリ作成
1.	Slack APIの準備
	•	Slack APIサイトにアクセスし、Slackワークスペースにログインします。
    https://api.slack.com/
2.	Slack APIアプリの作成
	•	「Your Apps」から新規にSlack Appを作成します。
	•	メッセージ送信などに必要な権限（スコープ）を設定し、アプリをワークスペースにインストールします。
    「from scratch」
    メニューの「OAuth & Permissions」の「Scopes」の「Bot Token Scopes」に「chat:write」を追加
    メニューの「OAuth Tokens」にて使用したいワークスペースにインストールする
	•	後で使用するため、Slack APIトークンを控えておきます。
    「Bot User OAuth Token」でBotとしてメッセージを送信する。

---

### 🐍 3. Python環境のセットアップとライブラリのインストール
#### 🔹 仮想環境の立ち上げ
    以下のコマンドでPython仮想環境を作成します。
    ```sh
    python3 -m venv <YOUR_VENV_DIRECTORY>
    ```
#### 🔹 仮想環境の有効化
    ```sh
    source <YOUR_VENV_DIRECTORY>/bin/activate
    ```
#### 🔹 必要なライブラリのインストール
    ```sh
    pip install sshtunnel psycopg2 pandas slack-sdk logging
    ```
#### 🔹 pythonスクリプトの実装
📌 `pg-slack-auto.py` → SSHでPGに接続し、SQLで成形したデータをSlackへ通知する
#### 🔹 python実行用シェルスクリプトの実装
📌 `run_script.sh` → python仮想環境を実行を立ち上げてからpythonスクリプトを実行する

---

### 🔄 4. launchctlによる自動実行の設定
#### 🔹 Launch Agentのplistファイル作成
📌 `com.mac.pg.slack.auto.plist` → 1時間ごとに実行用シェルスクリプトを実行。
#### 🔹 plistファイルを所定の場所に配置
    例：「/Users/<YOUR_USER>/Library/LaunchAgents/」配下
#### 🔹 Launch Agentの登録
    ```sh
    launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.mac.pg.slack.auto.plist
    ```
#### 🔹 設定変更時の再登録
    ```sh
    launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.mac.pg.slack.auto.plist
    launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.mac.pg.slack.auto.plist
    ```

---

✅ **セットアップ完了！** 🎉




