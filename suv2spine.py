#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import math
import json

VERSION = 1.01
DEFAULT_SCALE = 10.0

# 書き出しJSONテンプレート Spine3.5.51で簡易形式(non-essential)で書き出したものを元に作成
# hash値はかぶってもインポート時に別のものとして取り込めるので固定でも大丈夫ぽい
# hull値とedge値はなくてもとりあえずは大丈夫 (インポート時に警告は出る)
# @see http://ja.esotericsoftware.com/spine-json-format
# (hash: A hash of all the skeleton data. This can be used by tools to detect if the data has changed since the last time it was loaded.)
# (hull: The number of vertices that make up the polygon hull. The hull vertices are always first in the vertices list.)
# (edges: A list of vertex index pairs that define the edges between connected vertices. Nonessential.)
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
				"hull": %(HULL)s,
				"edges": %(EDGES)s
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
def convert(suv_json, hash, data_version, scale):
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
	
	# メッシュ拡大
	for i in range(0, len(v2)):
		v2[i] *= scale
	
	# UV上下反転
	for i in range(1, len(uv), 2): # 偶数番目＝v座標のみ変換
		uv[i] = 1.0 - uv[i] 
	
	# hull値(外周の頂点数)
	hull = 0 # 外周が判定できないので0とする(外周の頂点はverticesの先頭に並んでいなくてはならない)
	
	# edge (外周のライン情報 2頂点1組で1ラインを表す)
	edge = '[]' #とりあえず設定しない

	output_str = output_template %{\
		'DATA_VERSION': data_version,\
		'HASH': hash, \
		'SLOT': slot, \
		'UVS': uv, \
		'TRIANGLES': tri, \
		'VERTICES': v2, \
		'IMAGE': image_name, \
		'HULL': hull, \
		'EDGES': edge}
	
	# 変換後の文字列からjson生成
	output_json = json.loads(output_str)
	return output_json


parser = argparse.ArgumentParser(description=u'suv2spine ver. %6.2f 使い方' % VERSION)
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

parser.add_argument('-s', '--scale', \
	action='store', \
	nargs=None, \
	const=None, \
	default=10.0, \
	type=float, \
	choices=None, \
	help=u'拡大サイズ(デフォルト%6.1f)' % DEFAULT_SCALE, \
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
scale =args.scale

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
output_json = convert(suv_json, hash, data_version, scale)

# ファイル書き出し
fh = open(file_out, 'w')
json.dump(output_json, fh, indent=4, ensure_ascii=True)
fh.close()

print '''\
コンバート完了
出力ファイル: \'%s\' ''' % file_out
