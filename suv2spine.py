#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import math
import json

# 書き出しJSONテンプレート Spine3.5.51で簡易形式(non-essential)で書き出したものを元に作成
# hash値はかぶってもインポート時に別の元して取り込めるので固定でも大丈夫ぽい
# hull値はなくても大丈夫なようだが、ちゃんと設定するのは大変 データのソートも必要かも
# @see http://ja.esotericsoftware.com/spine-json-format
# (hash: A hash of all the skeleton data. This can be used by tools to detect if the data has changed since the last time it was loaded.)
# (hull: The number of vertices that make up the polygon hull. The hull vertices are always first in the vertices list.)
output_template = """\
{
"skeleton": { "hash": "%(HASH)s", "spine": "%(DATA_VERSION)s", "width": 0, "height": 0 },
"bones": [
	{ "name": "root" }
],
"slots": [
	{ "name": "%(SLOT)s", "bone": "root", "attachment": "%(IMAGE)s" }
],
"skins": {
	"default": {
		"%(SLOT)s": {
			"%(IMAGE)s": {
				"type": "mesh",
				"uvs": %(UVS)s,
				"triangles": %(TRIANGLES)s,
				"vertices": %(VERTICES)s,
				"hull": %(HULL)s
			}
		}
	}
},
"animations": {
	"animation": {}
}
}
"""

# jsonのコンバート
def convert(suv_json, hash, data_version):
	mesh = suv_json['mesh'][0]
	tri = mesh['tri']
	v2 = mesh['v2']
	uv = mesh['uv']
	
	# イメージ名
	image_name = suv_json['mat']['txName'][0]
	# イメージ名から拡張子を取り除く
	temp = image_name.split('.')
	temp.pop(len(temp) - 1)
	image_name = '.'.join(temp)
	
	# slot名決め打ち
	slot = 'slot1'
	
	#上下反転
	for i in range(1, len(uv), 2): # 偶数番目＝v座標のみ変換
		uv[i] = 1.0 - uv[i] 
	
	hull = 0 #len(tri) / 3 #temp

	output_str = output_template %{\
		'DATA_VERSION': data_version,\
		'HASH': hash, \
		'SLOT': slot, \
		'UVS': uv, \
		'TRIANGLES': tri, \
		'VERTICES': v2, \
		'IMAGE': image_name, \
		'HULL': hull}
	
	# 変換後の文字列からjson生成
	output_json = json.loads(output_str)
	return output_json


parser = argparse.ArgumentParser(description=u'このプログラムの使い方')
parser.add_argument('file', \
	action='store', \
	nargs='?', \
	const=None, \
	default='', \
	type=str, \
	choices=None, \
	help=u'SpriteUV2で書き出したjsonファイルへのパス', \
	metavar=None)

parser.add_argument('-o', '--out', \
	action='store', \
	nargs='?', \
	const=None, \
	default=None, \
	type=str, \
	choices=None, \
	help=u'アウトプットファイルのパス', \
	metavar=None)

parser.add_argument('-dv', '--data_version', \
	action='store', \
	nargs='?', \
	const=None, \
	default='3.5.51', \
	type=str, \
	choices=None, \
	help=u'Spineデータversion(デフォルト値\'3.5.51\'以外は未検証)', \
	metavar=None)

parser.add_argument('--hash', \
	action='store', \
	nargs='?', \
	const=None, \
	default='o7OrG0ujxVN067gHTwarZZcwz7o', \
	type=str, \
	choices=None, \
	help=u'Skeletonデータのハッシュ値', \
	metavar=None)

args = parser.parse_args()
file_in = args.file
file_out = args.out
data_version = args.data_version
hash = args.hash

# デフォルトアウトプット名の作成 path/to/json/hoge.json -> path/to/json/hoge_out.json
if file_out is None: 
	temp = file_in.split('.')
	temp[len(temp) -2] += '_out'
	file_out = '.'.join(temp)

# 引数がない場合はエラーにせずhelpを表示
if file_in =='':
	parser.print_help()
	quit()

# ファイルが存在しない場合エラー文言とusageを表示
if not os.path.isfile(file_in):
	print u'error: ファイルが存在しないか不正です: "%s"' % file_in
	parser.print_usage()
	quit()




# ファイル読み込み
fh = open(file_in, 'r')
suv_json = json.load(fh)
fh.close()

# データコンバート
output_json = convert(suv_json, hash, data_version)

# ファイル書き出し
fh = open(file_out, 'w')
json.dump(output_json, fh, indent=4, ensure_ascii=True)
fh.close()

print '''\
コンバート完了
出力ファイル: \'%s\' ''' % file_out
