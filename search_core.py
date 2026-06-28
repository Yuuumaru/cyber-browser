# -*- coding: utf-8 -*-
"""
オリジナル検索エンジンコアモジュール
簡易的な転置インデックス（Inverted Index）構造を持ち、クエリに対して瞬時にスコア判定を行います。
"""
import re
from collections import defaultdict

class CyberSearchEngine:
    def __init__(self):
        # 簡易データベース（インデックス元データ）
        self.documents = {
            "https://github.com/trending": "GitHub Trending - Discover the best projects on GitHub today.",
            "https://github.com/pyside/pyside-setup": "PySide6 Official Repository. Qt for Python.",
            "https://pyside.org": "Official PySide6 documentation and community hubs.",
            "https://git-scm.com": "Git version control system - modern distributed development tool.",
            "https://cyberpunk.fandom.com": "Cyberpunk database - UI design, netrunning, and neon aesthetics.",
            "https://stackoverflow.com": "Stack Overflow - Where Developers Learn, Share, & Build Careers."
        }
        self.index = defaultdict(list)
        self._build_index()

    def _normalize(self, text):
        # 小文字化と記号の除去
        return re.findall(r'\w+', text.lower())

    def _build_index(self):
        # 単語からURLへのマッピングを作成
        for url, content in self.documents.items():
            words = self._normalize(content) + self._normalize(url)
            for word in set(words):
                self.index[word].append(url)

    def search(self, query: str) -> list:
        if not query.strip():
            return []

        # 特殊コマンドの処理（例: github: から始まる場合はフィルタリング）
        force_github = False
        if query.startswith("github:"):
            force_github = True
            query = query.replace("github:", "").strip()

        query_words = self._normalize(query)
        if not query_words:
            return list(self.documents.keys())[:3]

        # マッチングスコア計算
        scores = defaultdict(int)
        for word in query_words:
            if word in self.index:
                for url in self.index[word]:
                    scores[url] += 1

        # スコア順にソート
        results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        filtered_results = [url for url, score in results]

        if force_github:
            filtered_results = [url for url in filtered_results if "github" in url]

        # もし独自エンジンで何もヒットしなければ、通常のDuckDuckGo等のフォールバック用URLを返す
        if not filtered_results:
            return [f"https://duckduckgo.com/?q={query}"]

        return filtered_results