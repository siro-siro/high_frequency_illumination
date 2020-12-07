#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
A window generation module for displaying patterns.
パターンを表示するためのウィンドウを作るモジュール．

After making this window, a pattern is rendered by 'display' command of imagemagick.
ウィンドウを作成後，imagemagick の display コマンドにより，このウィンドウ内に画像が描画されます．
 $ display -window SC_display_window.py pattern.png
'''
import sys
from PyQt4 import QtGui, QtCore
 
 
class Window( QtGui.QWidget ):
    
    def __init__( self, parent=None ):
        '''
        Initialize.
        ウィンドウを初期化します．
        '''
        super( Window, self ).__init__( parent )
        self.resize( 200, 200 ) 
        layout     = QtGui.QVBoxLayout( self )
        self.label = QtGui.QLabel( 'Here' )
        self.label.setStyleSheet(
            'font-family:arial black; font-size:64px'
        )         
        layout.addWidget( self.label )
        layout.setAlignment( self.label, QtCore.Qt.AlignCenter )
    
    def set_position(self, flip=False):        
        '''
        Try to set the window position in order to display in the secondary screen.
        ウィンドウの位置を決めます．
        セカンダリスクリーンに表示されるよう試みます．
        
        Parameters
        ----------
        flip : bool, optional
            If the secondary screen is placed 'left' of the main screen, set True.
            実行環境がセカンダリモニタで，プロジェクタがプライマリモニタの時は True にします．
        '''
        # スクリーン情報を取得
        desktop = QtGui.qApp.desktop()        
        w = desktop.width()
        h = desktop.height()
        if flip:
            self.move(-w, -h)
        else:
            self.move(w, h)
        
 
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='ウィンドウを作成します．')
    parser.add_argument('-f', '--flip', action='store_true', help='ウィンドウの表示位置を反転します．プロジェクタがプライマリスクリーンであったり，"左側"に配置されてる場合はこのオプションを指定します．')  
    parser.add_argument('-t', '--test', action='store_true', help='テストモード．最大化をせずに表示します．')
    args = parser.parse_args()
    
    app = QtGui.QApplication( sys.argv )
    win = Window()
    win.set_position(args.flip)
    if args.test:
        win.show()
    else:
        win.showFullScreen()
     
    sys.exit( app.exec_() )