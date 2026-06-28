# -*- coding: utf-8 -*-
import sys
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QTextBrowser)
from PySide6.QtWebEngineWidgets import QWebEngineView  # Web表示用
from search_core import CyberSearchEngine

# 近未来的デザインを定義するQSS (Cyberpunk / Matrix Mix Style)
CYBER_STYLE = """
QMainWindow {
    background-color: #0b0f19;
}
QWidget {
    color: #00ffcc;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 14px;
}
QLineEdit {
    background-color: #121824;
    border: 2px solid #00ffcc;
    border-radius: 4px;
    padding: 8px;
    color: #ffffff;
    selection-background-color: #ff0055;
}
QLineEdit:focus {
    border: 2px solid #ff0055;
    box-shadow: 0 0 10px #ff0055;
}
QPushButton {
    background-color: #121824;
    border: 1px solid #00ffcc;
    border-radius: 4px;
    padding: 8px 16px;
    color: #00ffcc;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #00ffcc;
    color: #0b0f19;
}
QPushButton:pressed {
    background-color: #ff0055;
    border-color: #ff0055;
    color: #ffffff;
}
QTextBrowser {
    background-color: #0d131f;
    border: 1px dashed #00ffcc;
    border-radius: 4px;
    color: #39ff14;
}
"""

class CyberBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CYBER_OS // BROWSER_CORE_v1.0")
        self.resize(1100, 750)
        self.setStyleSheet(CYBER_STYLE)

        # 検索エンジンの初期化
        self.search_engine = CyberSearchEngine()

        # メインレイアウト構築
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # 上部ナビゲーション・検索バー
        nav_layout = QHBoxLayout()
        
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("INPUT TARGET URL OR COMMAND (e.g., github:pyside)...")
        self.address_bar.returnPressed.connect(self.execute_search)
        
        self.btn_search = QPushButton("EXECUTE")
        self.btn_search.clicked.connect(self.execute_search)
        
        nav_layout.addWidget(self.address_bar)
        nav_layout.addWidget(self.btn_search)
        main_layout.addLayout(nav_layout)

        # 画面分割: 左側に検索ログ・結果、右側にWEBビュー（または結果表示）
        content_layout = QHBoxLayout()
        
        # オリジナルエンジンの結果出力コンソール
        self.console_output = QTextBrowser()
        self.console_output.setMaximumWidth(320)
        self.console_output.append("== CYBER SEARCH CORE SYSTEM READY ==")
        self.console_output.append("TIP: Use 'github:<query>' for prioritized repo source.")
        
        # Web表示用コンポーネント
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("about:blank"))
        
        content_layout.addWidget(self.console_output)
        content_layout.addWidget(self.web_view)
        
        main_layout.addLayout(content_layout)

    def execute_search(self):
        query = self.address_bar.text().strip()
        if not query:
            return

        self.console_output.append(f"\n> SCANNING: '{query}'")
        
        # 直接URLが入力された場合はそのまま遷移
        if query.startswith("http://") or query.startswith("https://"):
            self.console_output.append(f">> DIRECT ACCESS REQUESTED.")
            self.web_view.setUrl(QUrl(query))
            return

        # オリジナル検索エンジンを稼働
        results = self.search_engine.search(query)
        
        if results:
            self.console_output.append(f">> {len(results)} NODES DETECTED.")
            for url in results:
                self.console_output.append(f" - [LINK] {url}")
            
            # 最も適合度の高い最初の結果をブラウザ側に展開
            target_url = results[0]
            self.console_output.append(f">> LOADING PRIME NODE: {target_url}")
            self.web_view.setUrl(QUrl(target_url))
        else:
            self.console_output.append(">> NO NODES FOUND. FALLBACK DEPLOYED.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = CyberBrowser()
    browser.show()
    sys.exit(app.exec())