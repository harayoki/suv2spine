# suv2spine

SpriteUV2 から書き出した メッシュデータjsonファイル を Spine にインポートできる json形式 に変更する Python scriptです。

## 開発環境
* Python のバージョン：2.7.10
* 開発OS：macOS Sierra ver.10.12.3
* Spine バージョン:3.5.51 Professional 
* SpriteUV2 バージョン: Pro 1.165f

※　SpineがProfessionalバージョンでない場合メッシュ機能が使えません

## ソフトウェアのリンク
SPINE　http://ja.esotericsoftware.com/
SpriteUV2 https://www.spriteuv.com/

## 簡単な使い方

./suv2spine.py sproteuv2export.json
-> sproteuv2export_out.json が作成されます

./suv2spine.py -o hoge.json sproteuv2export.json
-> hoge.json が作成されます

./suv2spine.py -s 5.0 sproteuv2export.json
-> メッシュの拡大率を5倍にします（デフォルトは10倍です)

その他はヘルプを参照してください。

./suv2spine.py -h

