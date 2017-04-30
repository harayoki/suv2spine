SpriteUV2 から書き出した メッシュデータjsonファイル を Spine にインポートできる json形式 に変更する Python scriptです。

開発に利用したPython のバージョン：2.7.10
開発OS：macOS Sierra ver.10.12.3
Spineバージョン:3.5.51 Professional (Professionalでないとメッシュ機能は使えません）

簡単な使い方

./suv2spine.py sproteuv2export.json
-> sproteuv2export_out.json が作成されます

./suv2spine.py -o hoge.json sproteuv2export.json
-> hoge.json が作成されます

./suv2spine.py -s 5.0 sproteuv2export.json
-> メッシュの拡大率を5倍にします（デフォルトは10倍です)

その他はヘルプを参照してください。

./suv2spine.py -h




