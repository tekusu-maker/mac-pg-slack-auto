# mac-pg-slack-auto

## 概要
このリポジトリは、Pythonを用いてSSH接続を確立し、リモートのPostgreSQLデータベースから必要なデータを取得します。取得した情報をSlack APIを通じて通知することで、システムの監視や運用を効率化します。また、Mac上でlaunchdを利用して自動起動する設定も含まれており、定期実行環境を実現しています。

## セットアップ手順

### 1. SSH鍵の作成とAWS EC2への登録
1. **ED25519形式のSSH鍵の作成**  
   以下のコマンドで鍵を生成します。  
   ```
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
※ 鍵の保存先は /Users/<YOUR_DIRECTORY_PATH>/.ssh/id_ed25519 など、環境に合わせて指定してください。

2.	**AWS EC2への鍵登録**
   AWSマネジメントコンソールにログインし、EC2の「Key Pairs」セクションに移動します。
   作成した公開鍵（id_ed25519.pub）をインポートし、EC2インスタンスで利用できるようにします。
