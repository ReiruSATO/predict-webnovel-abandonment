import MeCab
from collections import Counter

# ワーカー関数をファイルに書き出す
def process_chunk(texts):
    # プロセスごとにTaggerを初期化
    tagger = MeCab.Tagger()
    local_counter = Counter()

    # ストップワード
    stop_words = {'する', 'いる', 'ある', 'なる', 'ない', 'れる', 'られる', 'こと', 'もの', 'それ', 'これ', 'よう', 'ため'}

    for text in texts:
        if not isinstance(text, str):
            continue

        node = tagger.parseToNode(text)
        while node:
            features = node.feature.split(',')
            pos = features[0]

            if pos in ['名詞', '動詞', '形容詞'] and node.surface not in stop_words:
                if features[1] not in ['非自立', '接尾', '数']:
                    base_form = features[6] if len(features) > 6 and features[6] != '*' else node.surface
                    local_counter[base_form] += 1
            node = node.next

    return local_counter
