#!/usr/local/bin/perl

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++　　[ 書き込み隊 ]
#+++
#+++		・・・・・>>> All Created by Tacky
#+++		・・・・・>>> Copyright (c) 1999.5 Tacky's Room. All rights reserved....
#+++
#+++        Homepage >>> http://tackysroom.com/
#+++
#+++ 設置方法構成(具体例)
#+++
#+++ public_html（ホームページディレクトリ）
#+++ |
#+++ |-- cgi-bin（任意のディレクトリ）
#+++   |
#+++   |-- jcode.pl        (755)…(日本語ライブラリ)
#+++   |-- kakikomitai.cgi (755)…(スクリプト本体)
#+++   |-- kakikomitai.txt (666)…(ログファイル)…空のままアップロード
#+++   |-- kakikomitai.cnt (666)…(カウンターファイル)…空のままアップロード
#+++
#+++ 　　■( )内はパーミッッションの値です。
#+++ 　　■gif以外はアスキーモード、gifはバイナリーモードでアップロードして下さい。
#+++ 　　■kakikomitai.lockは自動作成＆削除しますので、各自でご用意する必要はありません。
#+++ 　　■設置時にエラーになる方は、各ファイルの指定をフルパス(http://～)で指定してみて下さい。
#+++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

require 'jcode.pl';														#日本語コード変換

$url						= 'http://jrtu-tokyo.sakura.ne.jp/';		#戻り先ＵＲＬ
$url_target					= '_top';							#戻り先のURLを表示する際のターゲット
$script						= './kakikomitai.cgi';						#このＣＧＩの名前を指定
$method						= 'POST';									#METHODの指定(POST又はGET)
$logfile					= './kakikomitai.txt';						#ログファイルの名前を指定
$lockfile					= './kakikomitai.lock';						#ロックファイルの名前を指定
$title						= '2021春闘-みんなの声-';								#タイトルを指定
$titlelogo					= '';										#タイトル画像を指定
$backpicture				= '';										#背景画像を指定（使用しない場合は、''で良い)
$bgcolor					= '#ffffff';								#背景色を指定
$tbgcolor					= '#ffcc00';								#入力フォームの背景色を指定
$ttlcolor				    = '#ffffcc';								#ログ表示部の「タイトル」の文字色
$textcolor				    = '#ffffff';								#ログ表示部の「名前・メッセージ等」の文字色

$tcolor					    = '#996600';								# 文字色
$linkcolor				    = '#cc6600';								# リンク色（未読リンク）
$vlinkcolor					= '#666666';								# リンク色（既読リンク）
$alinkcolor		 			= '#ff3300';								# リンク色（押した時）

$titleset					= 1;								#新規投稿時に「タイトル」必要？(0:不要 1:必要)
$titleset2					= 1;							#レスする際に「タイトル」必要？(0:不要 1:必要)…新規投稿時タイトル必要の場合しか意味ありません
$pt							= '12pt';									#全体のフォントサイズ（pt指定以外何があるのか、僕知らない。(^^ゞ）

$homelinklogo				= './kakikomitai_linkhome.gif';				#ホームページ・リンク画像を指定
$maillinklogo				= './kakikomitai_linkmail.gif';				#メール・リンク画像を指定
$top_l						= './top_l_h.gif';							#メッセージ部左上隅の透過画像を指定
$top_r						= './top_r_h.gif';							#メッセージ部右上隅の透過画像を指定
$bottom_l					= './bottom_l_h.gif';						#メッセージ部左下隅の透過画像を指定
$bottom_r					= './bottom_r_h.gif';						#メッセージ部右下隅の透過画像を指定
$datamax					= 300 ;								#最大データ保存件数
$pagemax					= 20 ;								#１ページ内に表示する件数
$password					= 'pass';							#メンテナンス用パスワード（管理者用）
$tag						= 'no';								#タグ許可(yes,no)
$hostflag					= 'no' ;							#リモートホストを表示する？(yes.no)

#色の指定
@COLORS = ('#990033','#99cc00','#003366','#999999','#336633','#999966','#666699','#669999');

#入力フォームの各項目見出ししている部分に画像を使用しない場合は、０を設定
$gif_flg			= 0;										#(0:使用しない　1:使用する)

#入力フォームの各項目見出しに、ダウンロードした画像をそのまま
#使用する場合は、GIFを置くパスだけ修正してね
$gif_w				= '';	#画像の横幅
$gif_h				= '';	#画像の縦幅
$gif_name			= '';	#入力フォーム(name)
$gif_email			= '';	#入力フォーム(email)
$gif_home			= '';	#入力フォーム(homepage)
$gif_title			= '';	#入力フォーム(title)
$gif_message		= '';	#入力フォーム(message)
$gif_backcolor		= '';	#入力フォーム(backcolor)
$gif_password		= '';	#入力フォーム(password)
$gif_sage			= '';	#入力フォーム(sage)

#<<<↓の画像はそのまま使用してね。パスだけ修正。
$gif_spacer			= './spacer.gif';				#ダミー透過画像
$gif_spacerb		= './spacer_b.gif';				#１×１黒色画像

#掲示板荒らし対策。排除したいプロバのアドレスを設定して下さい。
#　"xxx?.com"とした場合、"xxx1.com","xxx2.com"等、「？」の部分が文字列１つと判断します
#  "xxx*.com"とした場合、"xxx1.com","xxx12345.com等、「＊」の部分が０個以上の文字列と判断します。
@DANGER_LIST=("xxx.com","yyy.com","zzz*.or.jp");

#掲示板荒らし対策その２。メッセージ最大文字数を指定。特に設定しない場合は、''として下さい。
$maxword = '1000' ;

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Sendmailが使える方のみ以下の項目を設定して下さい。
#    ※Sendmailとは？
#　　　メールソフトを立ち上げないで、指定した相手にメールを送る事が出来る機能です。
#　　　自分のプロバイダーがSendmailに対応しているか、パスはどこ？等は、各自のプロバイダー
#　　　のＨＰでご確認して下さいね。
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#投稿時に管理者にメール送信する場合、sendmailのパスを指定
$sendmail = "";
#メール送信先アドレス。（管理者のアドレス）…「＠」の前には必ず「￥」を付けてね。
$smail_address = "xxxxx\@xxxxxx.xx.jp";

$hiho			= 0 ;					#プロバイダーが「hi-ho」の人のみ「1」にして下さい。　※Sendmail使う場合

$ressw			= 2 ;			#レス機能の設定(0:レス無し　1:管理人のみレス　2:みんなでレス)
$resflag		= 'yes' ;		#最新レスを先頭に表示する？(yes,no)

#メッセージ表示部分にある「返信」に画像を使う場合、画像ファイル名を指定。
#画像を使わない場合は、以下を''として下さい。
$res_gif		= './res.gif';

$row			= 4 ;				#入力フォーム・メッセージ欄の行数
$col			= 50 ;				#入力フォーム・メッセージ欄の文字数

$tbl_sz			= 400 ;			#ログ表示部のテーブル横幅(必ずピクセルで指定してね)

#投稿時のパスワードをcrypt関数を使用する（暗号化）
#crypt関数が利用出来ない場合もありますので、投稿時にエラーになる場合は、「0:使用しない」にして下さいね。
$ango			= 1 ;	#0:使用しない 1:使用する　（推奨：１：使用する）

#=============================================================================================================================================================================================
#フォームＣＳＳ設定　※使用しない場合は、$css_style = "";とし、そこから２行(先頭がEOMの行までを)を削除して下さい。
$css_style = <<"EOM";
STYLE=font-size:$pt;color:#000000;background-color:#ffffDD;border-style:solid;border-color:#000000;border-width:1;
EOM

$damedame		= 0 ;	#Locationヘッダが使えないサーバーは1。通常は0でいいはず。※トクトク、3nopage,WinNTサーバー等が1かな。

#◆◆◆↓セキュリティ◆◆◆
$postchk		= 1;		#投稿時・メンテナンス時のMethodをPOST限定にする場合は１。以外は０。
$urlchk			= '';	#ここで指定されたアドレス(CGIの設置アドレスを記入)以外から投稿があった場合をエラーとします。設定しない場合は''
$renchan		= 0 ;		#指定回数以上の連続投稿はエラーとする。設定しない場合は0としてね。
$urllink		= 2 ;		#タイトル及び本文にhttpからのリンクがあったらエラーにする？
							#(0:しない 1:URLは全てする 2:以下の$urlerrで指定された文字が含まれているURLのみエラーとする
#↓$urllink=2の場合、以下に指定した文字を含むURLをエラーとする
$urlerrnm[0]	= 'exe';
$urlerrnm[1]	= 'virus';
$kaigyo			= 0;		#指定値分の改行が連続した場合、１行改行に置換します。　※指定しない場合は0
$name_comment	= 'coxmment';#定期的に投稿してくるような事があったらこの名前を適当に変えてみて下さい。自動投稿スクリプトの種類によっては全然意味無いけど。
@errword 		= ('','');	#投稿禁止語句　ex.@errword = ('死ね','テストテスト');
$urlcnt			= 2;		#メッセージ欄に記入出来るURLの個数　※指定しない場合は0
$japan			= 1;		#メッセージ欄に"全角文字/半角カナ(但し半角カナは文字化けする事もあります)"が１文字でも無ければエラーとする？(0:no 1:yes)
$mailerr		= 0;		#メアド欄を入力されたらエラーにする？(0:no 1:yes)　※自動書込ツールはメアドを指定してくる事が多い為あえてエラーとしてみる
$urlerr			= 0;		#URL欄を入力されたらエラーにする？(0:no 1:yes)　※自動書込ツールはURLを指定してくる事が多い為あえてエラーとしてみる
#◆◆◆↑セキュリティ◆◆◆

#スクロールバーの色変更。よくわからない方は、"EOM"の次の行から先頭がEOMの行の間を削除してね。
$scrollbar = <<"EOM";
BODY{
scrollbar-base-color : #eeeeee;
}
EOM

#▼入力フォームの文字　※$gif_flg=0（画像を使わない場合）のみ
$lbl_name			= 'お名前';			#入力フォームの「名前」に表示する文字
$lbl_email			= 'メールアドレス';	#入力フォームの「Email」に表示する文字
$lbl_url			= 'ホームページ';	#入力フォームの「URL」に表示する文字
$lbl_ttl			= 'タイトル';		#入力フォームの「タイトル」に表示する文字
$lbl_comment		= 'メッセージ';		#入力フォームの「メッセージ」に表示する文字
$lbl_bcolor			= '背景色';			#入力フォームの「背景色」に表示する文字
$lbl_fcolor			= '文字色';			#入力フォームの「文字色」に表示する文字
$lbl_icon			= 'アイコン';		#入力フォームの「アイコン」に表示する文字
$lbl_iconlist		= 'アイコン一覧';	#入力フォームの「アイコン一覧」に表示する文字
$lbl_pass			= 'パスワード';		#入力フォームの「パスワード」に表示する文字
$lbl_submit			= '投　稿';			#入力フォームの「Submit」ボタンに表示する文字
$lbl_res			= '返　信';			#入力フォームの「RES」ボタンに表示する文字
$lbl_clear			= 'クリア';		#入力フォームの「Clear」ボタンに表示する文字
$lbl_sage			= 'sage';			#入力フォームの「sage」に表示する文字	★sage機能を使わない場合は''　★sageは$resflag≠"yes"の場合は無効
$lbl_sage2			= ' ※レスをした記事をトップに移動させない場合にチェック';	#入力フォームの「sage」の説明文

#入力フォームの下に表示させるメッセージ。表示しない場合は、この次の行～先頭がEOMの行までを削除してね。
$msg_top = <<"EOM";
<pre><b><font color=red>定昇4係数＋ベア3,000円獲得！</font></b></pre>
EOM

#<<<　ここから下はいじらない方がいいです。
@errtag = ('table','meta','form','!--','embed','html','body','tr','td','th','a');		#デンジャラ～なタグ

###############################################################################
#### Main Process  START  #####################################################
###############################################################################
$ENV{'TZ'} = "JST-9";
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);	#システム日時・時刻取得
$year  = sprintf("%02d",$year + 1900);	$month = sprintf("%02d",$mon + 1);	$mday  = sprintf("%02d",$mday);
$hour  = sprintf("%02d",$hour);	$min   = sprintf("%02d",$min);
$week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat') [$wday];
$today = "$month/$mday($week) $hour:$min";
&cookieget;																#<<<COOKIEの取得
&decode ;																#<<<デコード
if ( $FORM{'action'} eq "maintenance" && $FORM{'proc'} ne 'res') {		#<<<"処理"がメンテナンスの場合
	if ( $FORM{'proc'} ne 'stoppi' && $FORM{'proc'} ne 'unstoppi')	{
		&Maintenance;
	}	else	{
		if ( $FORM{'no'} eq '')	{	&error("ストッピを行う記事Noを入力して下さい。");	}
		if ( $FORM{'pass'} eq "")	{	&error("パスワードを入力して下さい。");	}
		if ( $FORM{'pass'} ne $password)	{	&error("パスワードが違います。");	}
		&update;
	}
}	elsif ( $FORM{'action'} eq "update" )	{							#<<<ログファイル更新（編集時）
	&update ;
}	elsif ( $FORM{'action'} eq 'regist' )	{
	&regist ;
}	else	{
	if ( $FORM{'proc'} eq 'res' ) {
		if ( $FORM{'pass'} eq "")	{	&error("パスワードを入力して下さい");	}
		if ( $FORM{'pass'} ne $password)	{	&error("管理者以外はこの機能\は使えません");	}
		$FORM{'resno'} = $FORM{'no'} ;
	}
	&header ;															#<<<htmlヘッダー出力
	&forminput ;														#<<<入力フォーム表示
	&view ;																#<<<ログ表示
	&footer ;															#<<<htmlフッター出力
}
exit;
###############################################################################
#### Main Process  END  #######################################################
###############################################################################

###<--------------------------------------------------------------
###<---   デコード＆変数代入
###<--------------------------------------------------------------
sub decode{
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});$post=1;
	} else { $buffer = $ENV{'QUERY_STRING'};$post=0; }
	@pairs = split(/&/,$buffer);
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$name =~ tr/+/ /;
		$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		if ($tag eq 'yes') {
			foreach ( @errtag )	{	if ($value =~ /<$_(.|\n)*>/i) {	 &error("使用出来ないタグが入力されています");	}	}
		}
		$chkvalue = $value;$chkvalue2 = $value;
		foreach $dat( @errword )	{
			if ( $dat ne '' ) {
				$chk = $dat;
				&jcode'convert(*chk, "euc");
				#全角/半角カナ含まない？
				if ($chk !~ /[\xA1-\xFE][\xA1-\xFE]/) {		$dat =~ tr/a-z/A-Z/;}
				&jcode'convert(*chkvalue, "euc");
				if ($chkvalue !~ /[\xA1-\xFE][\xA1-\xFE]/) {	$chkvalue2 =~ tr/a-z/A-Z/;	}
				#検索文字列
				if ( index($chkvalue2,$dat) >= 0 ) {
					&error("投稿禁止単語が入力されていますので投稿出来ません");
				}
			}
		}
		if ( $urllink && ($name eq 'name' || $name eq 'title' || $name eq 'hp' || $name eq $name_comment )) {
			if ( $urllink == 1 ) {
				if ( $value =~ /tp:\/\//i && $name ne 'hp' ) {
					&error("セキュリティ対策の為、URLは入力出来ません。");
				}
			}	else	{
				foreach $buf ( @urlerrnm ) {
					if ( $value =~ /([^=^\"]|^)(http|ftp)([\w|\!\#\&\=\-\%\@\~\;\+\:\.\?\/]+)/i ) {
						if ( $3 =~ /$buf/ ) {
							&error("文字「$buf」は、セキュリティ対策の為、入力出来ません。");
						}
					}
				}
			}
			$value =~ s/(\r\n){$kaigyo,}/$1/g if ( $kaigyo ) ;
		}
		if ( $name ne $name_comment )	{	$value =~ s/\r\n//g;	$value =~ s/\r|\n//g;	}
		if ( $tag ne 'yes' || $name ne $name_comment )	{
			$value =~ s/&/&amp;/g;	$value =~ s/"/&quot;/g;
			$value =~ s/</&lt;/g;	$value =~ s/>/&gt;/g;
		}
		$value =~ s/\,/&#44;/g;
		&jcode'convert(*value,'sjis');
		$FORM{$name} = $value;
	}
	if ( $FORM{'action'} eq 'regist' || $FORM{'action'} eq 'maintenance' ||
		 $FORM{'action'} eq 'update' )	{
		if ( $postchk && !$post )	{	&error("不正な投稿です。");	}
		if ( $urlchk && $ENV{HTTP_REFERER} !~ /$urlchk/i )	{	exit;	}
	}
	$FORM{$name_comment} =~ s/\r\n/<br>/g;	$FORM{$name_comment} =~ s/\r|\n/<br>/g;
	$FORM{'hp'}   =~ s/^http\:\/\///;
}
###<--------------------------------------------------------------
###<---   入力フォーム
###<--------------------------------------------------------------
sub forminput {
	print "<a href=$url target=$url_target>[HOME]</a>\n";
	if ( $FORM{'action'} eq 'res' ) {	print "&nbsp;&nbsp;<a href=\"javascript:history.back()\">[BACK]</a>" ; }
	print "<br><center>\n";
	if ( $titlelogo )	{
		print "<img src=\"$titlelogo\"><br>\n";
	}	else	{
		print "<font size=\"+1\" color=\"$tcolor\">$title</font><br>\n";
	}

	if ( $FORM{'action'} ne 'res' && $FORM{'action'} ne 'maintenance' && $msg_top ) {	print $msg_top ; }
	if ( $FORM{'action'} ne 'maintenance' || $FORM{'proc'} eq 'res')	{
		$c_name = $COOKIE{'nm'} ;	$c_email = $COOKIE{'em'} ;	$c_hp = $COOKIE{'hp'} ;
		$c_color = $COOKIE{'cl'} ;	$c_pass = $COOKIE{'ps'} ;	$c_title = '' ;	$c_comment = '' ;
	}
	$c_comment =~ s/&amp;/&/g;

	print "<form action=$script method=$method>\n";
	if ( $FORM{'action'} eq 'maintenance' )	{
		print "<br>\n";
		if ( $FORM{'proc'} ne 'res' ) {		print "<br>修正フォームです\n";		}
		else	{	print "<br>管理人専用返信フォームです\n";		}
		print "<br>\n";
	}	else	{
		if ( $FORM{'action'} eq 'res' ) {		print "<br>返信フォームです\n";		}
	}
	if ( $FORM{'action'} ne 'maintenance' || $FORM{'proc'} eq 'res' )	{
		print "<input type=hidden name=\"action\" value=\"regist\">\n";
		print "<input type=hidden name=\"resno\" value=$FORM{'no'}>\n";
	}	else	{
		print "<input type=hidden name=\"action\" value=\"update\">\n";
		print "<input type=hidden name=\"no\" value=\"$FORM{'no'}\">\n";
		print "<input type=hidden name=\"proc\" value=\"edit\">\n";
	}
	print "<table border=0 cellspacing=0 cellpadding=0>\n";

	print "<tr>\n";
	print "<td bgcolor=\"$tbgcolor\"><img src=$top_l width=8 height=8></td>\n";
	print "<td bgcolor=\"$tbgcolor\"><img src=\"$gif_spacer\" width=1 height=1></td>\n";
	print "<td bgcolor=\"$tbgcolor\"><img src=$top_r width=8 height=8></td>\n";
	print "</tr>\n";
	print "<tr>\n";
	print "<td width=8 bgcolor=\"$tbgcolor\"><img src=\"$gif_spacer\" width=1 height=1></td>\n";
	print "<td bgcolor=\"$tbgcolor\">\n";

	if ( $FORM{'action'} eq 'res'  || $FORM{'proc'} eq 'res' ) { $dmy = $lbl_res ; } else { $dmy = $lbl_submit ; }
	print "<table width=100% border=0 cellspacing=0 cellpadding=2>\n";
	print "<tr><td bgcolor=\"$tbgcolor\" align=left>\n";
	if ( $gif_flg == 1 )	{
		print "<img src=\"$gif_name\" border=0 width=$gif_w height=$gif_h></td>\n";
	}	else	{
		print "$lbl_name</td>\n";
	}
	print "<td bgcolor=\"$tbgcolor\">";
	print "<input type=text name=\"name\" size=30 value=\"$c_name\" $css_style></td></tr>\n";

	if ( $mailerr ) { $dmy1="style={display:none;}"; $c_email=""; } else { $dmy1=""; }
	print "<tr $dmy1><td bgcolor=\"$tbgcolor\" align=left>\n";
	if ( $gif_flg == 1 )	{
		print "<img src=\"$gif_email\" border=0 width=$gif_w height=$gif_h></td>\n";
	}	else	{
		print "$lbl_email</td>\n";
	}
	print "<td bgcolor=\"$tbgcolor\">";
	print "<input type=text name=\"email\" size=30 value=\"$c_email\" $css_style>\n";
	if ( $urlerr ) {
		if ( $titleset != 1 || ( $titleset == 1 && $titleset2 == 0 && ($FORM{'action'} eq 'res' || $FORM{'proc'} eq 'res')) ) {
			print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type=submit value=$dmy $css_style>&nbsp;&nbsp;\n";
			print "<input type=reset value=\"$lbl_clear\" $css_style>\n";
		}
	}
	print "</td></tr>\n";

	if ( $urlerr ) { $dmy1="style={display:none;}"; $c_hp=""; } else { $dmy1=""; }
	print "<tr $dmy1><td bgcolor=\"$tbgcolor\" align=left>\n";
	if ( $gif_flg == 1 )	{
		print "<img src=\"$gif_home\" border=0 width=$gif_w height=$gif_h></td>\n";
	}	else	{
		print "$lbl_url</td>\n";
	}
	print "<td bgcolor=\"$tbgcolor\">";
	print "<input type=text name=\"hp\" size=30 value=\"http://$c_hp\" $css_style>\n";
	if ( !$urlerr ) {
		if ( $titleset != 1 || ( $titleset == 1 && $titleset2 == 0 && ($FORM{'action'} eq 'res' || $FORM{'proc'} eq 'res')) ) {
			print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type=submit value=$dmy $css_style>&nbsp;&nbsp;\n";
			print "<input type=reset value=\"$lbl_clear\" $css_style>\n";
		}
	}
	print "</td></tr>\n";
	if ( $titleset == 1 )	{
		if ( $titleset2 == 0 && ($FORM{'action'} eq 'res' || $FORM{'proc'} eq 'res') ) {
		}	else	{
			print "<tr><td bgcolor=\"$tbgcolor\" align=left>\n";
			if ( $gif_flg == 1 )	{
				print "<img src=\"$gif_title\" border=0 width=$gif_w height=$gif_h></td>\n";
			}	else	{
				print "$lbl_ttl</td>\n";
			}
			print "<td bgcolor=\"$tbgcolor\">";
			print "<input type=text name=\"title\" size=30 value=\"$c_title\" $css_style>\n";
			print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type=submit value=$dmy $css_style>&nbsp;&nbsp;\n";
			print "<input type=reset value=\"-Clear-\" $css_style></td></tr>\n";
		}
	}
	print "<tr><td bgcolor=\"$tbgcolor\" align=left>\n";
	if ( $gif_flg == 1 )	{
		print "<img src=\"$gif_message\" border=0 width=$gif_w height=$gif_h></td>\n";
	}	else	{
		print "$lbl_comment</td>\n";
	}
	print "<td bgcolor=\"$tbgcolor\" align=left>";
	print "<textarea name=\"$name_comment\" cols=$col rows=$row $css_style>$c_comment</textarea></td></tr>\n";
	if ( $FORM{'action'} ne 'res' && $FORM{'proc'} ne 'res' && $c_resno eq '')	{
		print "<tr><td bgcolor=\"$tbgcolor\">\n";
		if ( $gif_flg == 1 )	{
			print "<img src=\"$gif_backcolor\" border=0 width=$gif_w height=$gif_h></td>\n";
		}	else	{
			print "$lbl_bcolor</td>\n";
		}
		print "</td>\n";
		print "<td bgcolor=\"$tbgcolor\">\n";
		foreach (0 .. $#COLORS) {
			if ( $c_color == $_ || ($c_color eq '' && $_ == 0)) {	$dmy = "checked";	}	else	{	$dmy = "" ;	}
			print "<input type=radio name=color value=\"$_\" $dmy>\n";
			print "<font color=$COLORS[$_]>■</font>\n";
		}
		print "</td></tr>\n";
	}
	if ( $FORM{'action'} ne 'maintenance' )	{
		print "<tr><td bgcolor=\"$tbgcolor\" align=left>\n";
		if ( $gif_flg == 1 )	{
			print "<img src=\"$gif_password\" border=0 width=$gif_w height=$gif_h></td>\n";
		}	else	{
			print "$lbl_pass</td>\n";
		}
		print "</td>\n";
		print "<td bgcolor=\"$tbgcolor\"><input type=password name=pass size=8 value=\"$c_pass\" $css_style><font size=-1>（修正・削除に使用します）</font></td></tr>\n";
	}	else	{
		print "<input type=hidden name=pass value=\"$FORM{'pass'}\">\n";
	}
	if ( $FORM{'action'} eq 'res' && $lbl_sage ne '' && $resflag eq 'yes' ) {
		print "<tr>\n";
		print "<td $tbgcolor>";
		if ( $gif_flg == 1 )	{
			print "<img src=\"$gif_sage\" border=0>\n";
		}	else	{
			print "$lbl_sage\n";
		}
		print "</td>\n";
		print "<td $tbgcolor>";
		print "<input type=checkbox name=\"sage\" value=\"1\">$lbl_sage2</td>\n";
		print "</tr>";
	}
	print "</table>\n";
	print "</td>\n";
	print "<td width=8 bgcolor=\"$tbgcolor\"><img src=\"$gif_spacer\" width=1 height=1></td>\n";
	print "</tr>\n";
	print "<tr>\n";
	print "<td bgcolor=\"$tbgcolor\"><img src=$bottom_l width=8 height=8></td>\n";
	print "<td bgcolor=\"$tbgcolor\"><img src=\"$gif_spacer\" width=1 height=1></td>\n";
	print "<td bgcolor=\"$tbgcolor\"><img src=$bottom_r width=8 height=8></td>\n";
	print "</tr>\n";
	print "</table>\n";
	print "</form></center>\n";
}
###<--------------------------------------------------------------
###<---   HTMLヘッダー書き出し
###<--------------------------------------------------------------
sub header {
	print "Content-type: text/html; charset=Shift_JIS\n\n";
	print "<html>\n<head>\n";
	print "<META HTTP-EQUIV=\"Content-type\" CONTENT=\"text/html; charset=x-sjis\">\n";
	print "<title>$title</title>\n";
	#<<<CSS START>>>
	print "<style type=\"text/css\">\n";
	print "<!--\n";
	print "body,tr,td { font-size: $pt;}\n";
	if ( $scrollbar ) { print $scrollbar; }
	print "-->\n";
	print "</style>\n";
	#<<<CSS END>>>
	print "</head>\n";
	if ($backpicture) { $set = "background=\"$backpicture\""; }
	elsif ($bgcolor )	{ $set = "bgcolor=\"$bgcolor\""; }
	print "<body $set text=$tcolor link=$linkcolor vlink=$vlinkcolor alink=$alinkcolor>\n";
}
###<--------------------------------------------------------------
###<---   HTMLフッダー書き出し
###<--------------------------------------------------------------
sub footer {
	#<<<　↓消さないでネ♪
	print "<div align=right>\n";
	print "<a href=http://tackysroom.com target=_top>kakikomitai Ver0.97 Created by Tacky</a>\n";
	print "</div>\n";
	print "</body></html>\n";
}
###<--------------------------------------------------------------
###<---   ログファイル読み込み
###<--------------------------------------------------------------
sub	dataread	{
	#<<<ログ読み込み
	if ( !(open(IN,"$logfile")))	{	&error("ログファイル($logfile)のオープンに失敗しました");	}
	@LOG = <IN>;
	close(IN);	$maxno = 0 ;
	foreach ( @LOG )	{
		($no,$name,$email,$hp,$ttl,$comment,$regdate,$color,$resno,$hst,$s,$pass,$d2) = split(/,/,$_);
		if ( $resno eq '' )	{	push(@MAINLOG,$_) ;	}
		else	{	push(@RESLOG,$_) ;	}
		if ( $no > $maxno ) { $maxno = $no ; }
	}
	@RESLOG = reverse @RESLOG ; #レスログは古い順に。
	$maxno++ ;
}
###<--------------------------------------------------------------
###<---   ログ表示
###<--------------------------------------------------------------
sub	view	{
	&dataread ;																#<<<ログ読み込み
	print "<center><hr width=70% size=1 noshade color=#000000>\n";
	#表示対象ページの先頭データ件数を算出
	$dm = @MAINLOG;
	if ( $dm % $pagemax == 0) {
		$p = $dm / $pagemax ;
	}	else	{
		$p = $dm / $pagemax + 1;
	}
	$p = sprintf("%3d",$p);
	if ( $FORM{'page'} eq "NEXT" )	{
		if ( $FORM{'disppage'} == 0 ) { $FORM{'disppage'} = 1 }	;
		$d = ($FORM{'disppage'} + 1) * $pagemax - $pagemax ;
		$FORM{'disppage'} = $FORM{'disppage'} + 1 ;
	}	elsif	( $FORM{'page'} eq "BACK" ) 	{
		$d = ($FORM{'disppage'} - 1) * $pagemax - $pagemax ;
		$FORM{'disppage'} = $FORM{'disppage'} - 1 ;
	}	elsif	( $FORM{'disppage'} ne "" ) 	{
		$d = $FORM{'disppage'} * $pagemax - $pagemax ;
	}	else	{
		$d = 0	;
		$FORM{'disppage'} = 1 ;
	}
	$z = 1 ;
	for ( $i = $d ; ( $z <= $pagemax ) && ( $i < $dm ); $i++ )	{
		($no,$name,$email,$hp,$ttl,$comment,$regdate,$color,$resno,$hst,$s,$pass,$d2) = split(/,/,$MAINLOG[$i]);
		if	( ( $FORM{'action'} ne 'res' && $FORM{'proc'} ne 'res' ) || ( ( $FORM{'action'} eq 'res'  || $FORM{'proc'} eq 'res' ) && $FORM{'no'} eq $no) )	{
			$color = $COLORS[$color] ;
			print "<br>\n";
			print "<table border=0 cellspacing=0 cellpadding=0 width=\"$tbl_sz\">\n";
			if	( $FORM{'action'} ne 'res' && $ressw == 2 )	{
				print "<form action=$script method=$method>";
				print "<input type=hidden name=\"action\" value=\"res\">";
				print "<input type=hidden name=\"no\" value=\"$no\">";
				print "<input type=hidden name=\"disppage\" value=$FORM{'disppage'}>\n";
			}
			print "<tr>\n";
			print "<td bgcolor=\"$color\"><img src=$top_l width=8 height=8></td>\n";
			print "<td bgcolor=\"$color\"><img src=\"$gif_spacer\" width=1 height=1></td>\n";
			print "<td bgcolor=\"$color\"><img src=$top_r width=8 height=8></td>\n";
			print "</tr>\n";
			print "<tr>\n";
			print "<td width=8 bgcolor=\"$color\"><img src=\"$gif_spacer\" width=1 height=1></td>\n";
			print "<td bgcolor=\"$color\">\n";
				print "<table cellpadding=0 cellspacing=0 border=0 width=\"$tbl_sz\">\n";
				print "<tr>\n";
				print "<td bgcolor=\"$color\">\n";
				if ( $titleset == 1 ) {
					if ( $ttl ) {
						print "<font color=\"$ttlcolor\">";
						print "■-$ttl</font>\n";
					}
					if ( $hostflag eq 'yes' && $hst )	{	print "&nbsp;&nbsp;&nbsp;<font color=\"$ttlcolor\" size=-1>..($hst)</font>";	}
					print "<br>\n"	if ( $ttl || ( $hostflag eq 'yes' && $hst ) );
				}
				print "<font color=\"$textcolor\">";
				$no = sprintf("%d",$no);
				print "&nbsp;>>&nbsp;$name&nbsp;&nbsp;</font><font color=\"$textcolor\" size=2>$regdate\[$no\]&nbsp;&nbsp;";
				print "</font>\n";
				print "</td>\n";
				print "</tr>\n";
				print "<tr><td bgcolor=\"$color\">\n";
				print "<img src=\"$gif_spacer\" width=\"$tbl_sz\" height=5><br>\n";
				print "<img src=\"$gif_spacerb\" width=\"$tbl_sz\" height=1><br>\n";
				$comment =~ s/([^=^\"]|^)(http|ftp)([\w|\!\#\&\=\-\%\@\~\;\+\:\.\?\/]+)/$1<a href=\"$2$3\">こちら<\/a>/g;
				$comment =~ s/&amp;/&/g;
				if ( $s eq '*' ) {
					print "<font color=\"$textcolor\" size=-1><br>\n";
					print "（この記事は常に先頭に表\示されます）<br><br></font>\n";
				}
				print "<font color=\"$textcolor\"><br>\n";
				print "$comment<br></font>\n";
				print "<div align=right>\n";
				if ( $email ne '' )	{	print "<a href=\"mailto:$email\"><img src=$maillinklogo width=50 height=12 border=0></a>\n";	}
				if ( $hp ne '' )	{	print "<a href=\"http://$hp\" target=_top><img src=$homelinklogo width=50 height=12 border=0></a>\n";	}
				if	( $FORM{'action'} ne 'res' && $ressw == 2 )	{
					if ( $res_gif )	{
						print "&nbsp;&nbsp;&nbsp;&nbsp;<input type=image name=send src=\"$res_gif\" border=0 alt=\"返信だよ\">\n";
					}	else	{
						print "&nbsp;&nbsp&nbsp;<input type=submit value=\"返信\">\n";
					}
				}
				print "</div></td></tr>\n";
				print "</table>\n";

				#レス表示
				if ( $ressw != 0 ) { $cnt = 0 ;
				foreach ( @RESLOG )	{
					($n,$name,$email,$hp,$ttl,$comment,$regdate,$rcolor,$resno,$hst,$s,$pass,$d2) = split(/,/,$_);
					if ( $no eq $resno )	{
						if ( $cnt == 0 ) { print "<br>\n";	}
						print "<table cellpadding=0 cellspacing=0 border=0 width=\"$tbl_sz\">\n";
						print "<tr>\n";
						print "<td bgcolor=\"$color\" width=50 nowrap>&nbsp;</td>\n";
						$w = $tbl_sz - 50 ;
						print "<td bgcolor=\"$color\"><img src=\"$gif_spacerb\" width=\"$w\" height=1></td></tr>\n";
						print "<tr>\n";
						print "<td bgcolor=\"$color\" width=50 nowrap>&nbsp;</td>\n";
						print "<td bgcolor=\"$color\">\n";
						if ( $titleset2 == 1 && $ressw != 1) {
							if ( !($ttl) )	{	$ttl = "";	}
							print "<font color=\"$ttlcolor\">";
							print "▲-$ttl</font>\n";
						}
						print "<font color=\"$textcolor\">(&nbsp;$name&nbsp;)</font>\n";
						if ( $hostflag eq 'yes' && $hst )	{	print "&nbsp;&nbsp;&nbsp;<font color=\"$textcolor\" size=-1>..($hst)</font>";	}
						print "</font></td></tr>\n";
						print "<tr><td bgcolor=\"$color\" width=50 nowrap>&nbsp;</td>\n";
						print "<td bgcolor=\"$color\">\n";
						$comment =~ s/([^=^\"]|^)(http|ftp)([\w|\!\#\&\=\-\%\@\~\;\+\:\.\?\/]+)/$1<a href=\"$2$3\">こちら<\/a>/g;
						$comment =~ s/&amp;/&/g;
						print "<font color=\"$textcolor\"><br>$comment</font><br>\n";
						$n = sprintf("%d",$n);
						print "<div align=right><font color=\"$textcolor\" size=2>..$regdate";
						print "[$n]</font>\n";
						if ( $ressw != 1 )	{
							if ( $email ne '' )	{	print "<a href=\"mailto:$email\"><img src=$maillinklogo width=50 height=12 border=0></a>\n";	}
							if ( $hp ne '' )	{	print "<a href=\"http://$hp\" target=_top><img src=$homelinklogo width=50 height=12 border=0></a>\n";	}
						}
						print "</div></td></tr>\n";
						print "</table>\n";
						$cnt++ ;
					}
				}
				}
			print "</td>\n";
			print "<td width=8 bgcolor=\"$color\"><img src=\"$gif_spacer\" width=1 height=1></td>\n";
			print "</tr>\n";
			print "<tr>\n";
			print "<td bgcolor=\"$color\"><img src=$bottom_l width=8 height=8></td>\n";
			print "<td bgcolor=\"$color\"><img src=\"$gif_spacer\" width=1 height=1></td>\n";
			print "<td bgcolor=\"$color\"><img src=$bottom_r width=8 height=8></td>\n";
			print "</tr>\n";
			print "</form>\n" if ( $FORM{'action'} ne 'res' && $ressw == 2 ) ;
			print "</table>\n";
		}
		$z++;
	}

	if ( $FORM{'action'} ne 'res' && $FORM{'proc'} ne 'res' ) {
		$dm = @MAINLOG;
		if ( $dm % $pagemax == 0) {
			$p = $dm / $pagemax ;
		}	else	{
			$p = $dm / $pagemax + 1;
		}
		$p = sprintf("%3d",$p);
		print "<br><form action=$script method=$method>\n";
		print "<input type=hidden name=\"disppage\" value=$FORM{'disppage'}>\n";
		if ( $FORM{'disppage'} != 0 && $FORM{'disppage'} !=1)	{
			print "<input type=submit name=\"page\" value=BACK $css_style>\n";
		}
		if ( $FORM{'disppage'} + 1 <= $p )	{
			print "<input type=submit name=\"page\" value=NEXT $css_style>\n";
		}
		print "</form><hr width=70% size=1 noshade color=#000000>\n";
		print "</center>\n";
		print "<div align=\"right\"><font  color=\"$tcolor\">";
		print "<form action=\"$script\" method=\"$method\">\n";
		print ">><font size=-1>修正・削除は、記事Noと投稿時に入力したパスワードを入力し<br>edit又はdeleteを選択し、updateボタンを押下して下さい</font>\n";
		print "<br>No.<input type=text name=\"no\" size=3 $css_style>\n";
		print "Pass<input type=password name=\"pass\" size=10 $css_style>\n";
		print "</font>\n";
		print "<select name=\"proc\" $css_style>\n";
		print "<option value=\"res\">res\n"	if ( $ressw == 1 ) ;
		print "<option value=\"edit\">edit\n";
		print "<option value=\"delete\">delete\n";
		print "<option value=\"stoppi\">stoppi\n";
		print "<option value=\"unstoppi\">unstoppi\n";
		print "</select>\n";
		print "<input type=hidden name=\"action\" value=\"maintenance\">\n";
		print "<input type=submit value=\"update\" $css_style>\n";
		print "</form></div>\n";
	}	else	{	print "<br><br><br>\n";	}
}
###<--------------------------------------------------------------
###<---   ログ出力
###<--------------------------------------------------------------
sub	regist	{
	# ホスト名を取得
	$host  = $ENV{'REMOTE_HOST'};
	$addr  = $ENV{'REMOTE_ADDR'};
	if ($host eq "" || $host eq "$addr") {
		($p1,$p2,$p3,$p4) = split(/\./,$addr);
		$temp = pack("C4",$p1,$p2,$p3,$p4);
		$host = gethostbyaddr("$temp", 2);
		if ($host eq "") { $host = $addr; }
	}
	#掲示板荒らし対策
	foreach $buf(@DANGER_LIST){
		# パターンマッチを変換
		$buf=~ s/\./\\./g;		$buf=~ s/\?/\./g;		$buf=~ s/\*/\.\*/g;
		if($host =~ /$buf/gi){
			&error("\申\し\訳ありません。<br>あなたのプロバイダーからは投稿できませんでした． ");
		}
	}
	if ( $maxword ne '' && (length($FORM{$name_comment}) > $maxword))	{	&error("メッセージは$maxword文字までしか登録出来ません。");	}
	if ( $FORM{'name'} eq '')	{	&error("お名前を入力して下さい。");	}
	if ( $FORM{$name_comment} eq '')	{	&error("メッセージは省略出来ません。");	}
	# URLと同じものが本文にあったら宣伝
	if ($FORM{'hp'}){
		if ( $FORM{$name_comment} =~ /$FORM{'hp'}/) {
			&error("宣伝投稿と見なされますので投稿出来ません");
		}
	}
	if ( $urlcnt ) {
		$urlnum = ($FORM{$name_comment} =~ s/(h?ttp)/$1/ig);
		if ( $urlnum > $urlcnt ) { &error("URLは" . ($urlcnt + 1) . "個以上は記入出来ません"); }
	}
	if ( $japan ) {
		$str = $FORM{$name_comment};
		jcode::convert(\$str, 'euc','sjis');
		if($str =~ /[\xA1-\xFE][\xA1-\xFE]/ || $str =~ /\x8E/ || $str =~ /[\x8E\xA1-\xFE]/){
		}	else	{
			&error("半角英数字のみの投稿は出来ません。");
		}
	}
	if ( $mailerr == 1 && $FORM{'email'} ) { &error("セキュリティ対策の為、メールアドレスは入力出来ません。");	}
	if ( $urlerr == 1 && $FORM{'hp'} ) { &error("セキュリティ対策の為、URLは入力出来ません。");	}

	&filelock ;	#ファイルロック
	&dataread ;																#<<<ログ読み込み
	foreach ( @LOG )	{
		($oyano,$name,$email,$hp,$ttl,$comment,$regdate,$color,$resno,$hst,$s,$pass,$d2) = split(/,/,$_);
		if ( $hst ne $host )	{	$chk=1; }
		if ( $renchan !=0 && $hst eq $host && $chk != 1 )	{
			$write_cnt++ ;
			if ( $write_cnt + 1 >= $renchan )	{	&fileunlock ;	&error("$renchan回以上の連続投稿は禁止しています");	}
		}
		if ( $name eq $FORM{'name'} && $comment eq $FORM{$name_comment} )	{
			&fileunlock ;	&error("二重投稿は禁止しています。") ;			last ;
		}
	}

	$dcnt = @LOG;
	if ($dcnt >= $datamax) {	pop(@LOG);	}

	$stoppi = 0 ;
	($no,$name,$email,$hp,$ttl,$comment,$regdate,$color,$resno,$hst,$s,$pass,$d2) = split(/,/,$LOG[0]);
	if ( $s eq '*' ) { $stoppi = 1 ; }

	#レス記事登録時で、ログを先頭に移動する場合の処理
	if ( $resflag eq 'yes' && $FORM{'resno'} ne '' && $FORM{'sage'} != 1)	{
		$cnt = 0 ;
		foreach ( @LOG )	{
			($oyano,$name,$email,$hp,$ttl,$comment,$regdate,$color,$resno,$hst,$s,$pass,$d2) = split(/,/,$_);
			if ( $oyano eq $FORM{'resno'} )	{
				$sv_title = $ttl ;
				splice(@LOG,$cnt,1);
				$wk = "$oyano,$name,$email,$hp,$ttl,$comment,$regdate,$color,$resno,$hst,$s,$pass,$d2" ;
				unshift(@LOG,$wk);
				last ;
			}
			$cnt++ ;
		}
	}	else	{
		if ( $sendmail ) {
			foreach ( @LOG )	{
				($oyano,$name,$email,$hp,$ttl,$comment,$regdate,$color,$resno,$hst,$s,$pass,$d2) = split(/,/,$_);
				if ( $oyano eq $FORM{'resno'} )	{
					$sv_title = $ttl ;		last ;
				}
			}
		}
	}

	# パスワードの暗号化（crypt関数使用））
	if ($FORM{'pass'} ne "") { &pass_enc($FORM{'pass'}); }	else	{ $pass = '' ; }
	unshift(@LOG,"$maxno,$FORM{'name'},$FORM{'email'},$FORM{'hp'},$FORM{'title'},$FORM{$name_comment},$today,$FORM{'color'},$FORM{'resno'},$host,,$pass,\n");

	#ストッピ機能！　常に一番上に持っていくよ
	if ( $stoppi == 1 )	{
		$cnt = 0 ;
		foreach ( @LOG )	{
			($oyano,$name,$email,$hp,$ttl,$comment,$regdate,$color,$resno,$hst,$s,$pass,$d2) = split(/,/,$_);
			if ( $s eq '*' )	{
				splice(@LOG,$cnt,1);
				$wk = "$oyano,$name,$email,$hp,$ttl,$comment,$regdate,$color,$resno,$hst,$s,$pass,$d2" ;
				unshift(@LOG,$wk);
				last ;
			}
			$cnt++ ;
		}
	}

	if ( !(open(OUT,">$logfile")))	{	&fileunlock ;	&error("ログファイル($logfile)のオープンに失敗しました");	}
	print OUT @LOG;
	close(OUT);

	&fileunlock ;	#ファイルロック解除
	if ( $sendmail ) { &SMail ;	}

	#COOKIE設定
	&cookieset ;
	if ( $damedame == 0 )	{
		print "Location: $script?\n\n";
	}	else	{
		print "Content-type: text/html\n\n";
		print "<html><head><META HTTP-EQUIV=\"Refresh\" CONTENT=\"0; URL=";
		print "$script\"></head><body></body></html>\n\n";
	}
}
###<--------------------------------------------------------------
###<---   メンテナンスモード
###<--------------------------------------------------------------
sub Maintenance {
	if ( $FORM{'pass'} eq "")	{	&error("パスワードを入力して下さい。");	}
	$found = 0 ;
	&dataread ;																#<<<ログ読み込み
	foreach ( @LOG )	{
		($no,$name,$email,$hp,$ttl,$comment,$regdate,$color,$resno,$hst,$s,$pass,$d2) = split(/,/,$_);
		if ( $FORM{'no'} eq $no )	{
			if ($FORM{'pass'} ne $password && (&pass_dec($pass))) { &error("パスワードが違います。"); }
			$found = 1 ;
			if ( $FORM{'proc'} eq "delete" )	{
				&update ;
				exit;
			}
			&header ;
			$c_name = $name ;	$c_email = $email ;	$c_hp = $hp ;	$c_title = $ttl ;
			$c_color = $color ;	$c_comment = $comment ; $c_resno = $resno ;
			$c_comment =~ s/\<br\>/\n/g;	$c_pass = $FORM{'pass'} ;	$c_resno = $resno ;
			&forminput ;
			last;
		}
	}
	if ( $found == 0 )	{
		&error("該当する記事Noのデータは存在していません。");
	}
	&footer ;
	exit;
}

###<--------------------------------------------------------------
###<---   ログファイル更新
###<--------------------------------------------------------------
sub update {
	&filelock ;	#ファイルロック
	&dataread ;																#<<<ログ読み込み

	$found = 0 ;	$cnt = 0 ;
    foreach (@LOG) {
		($no,$name,$email,$hp,$ttl,$comment,$regdate,$color,$resno,$hst,$s,$pass,$d2) = split(/,/,$_);
		if ( $FORM{'proc'} eq 'stoppi' && $s eq '*' ) { &fileunlock ;	&error("既にストッピされている記事がありますので、ストッピ出来ません。") ;	}
		if ( $FORM{'no'} eq $no)	{								#<<<メンテ対象者の場合
			if ($FORM{'pass'} ne $password && (&pass_dec($pass))) {
				&fileunlock ;	#ファイルロック解除
				&error("パスワードが違います。");
			}
			if ( $FORM{'proc'} eq 'stoppi' && $resno ne '') { &fileunlock ;	&error("親記事以外はストッピ出来ません。"); }
			if ( $FORM{'proc'} eq 'unstoppi' && $s ne '*') { &fileunlock ;	&error("その記事はストッピ記事ではありません。"); }
			$found = 1 ;
			if ( $FORM{'proc'} eq 'edit' )	{
				push(@new,"$no,$FORM{'name'},$FORM{'email'},$FORM{'hp'},$FORM{'title'},$FORM{$name_comment},$regdate,$FORM{'color'},$resno,$hst,$s,$pass,$d2");
			}	elsif ( $FORM{'proc'} ne 'delete' ) 	{
				if ( $FORM{'proc'} eq 'stoppi' ) { $dmy = "*" ; } else { $dmy = "" ; }
				$wk = "$no,$name,$email,$hp,$ttl,$comment,$regdate,$color,$resno,$hst,$dmy,$pass,$d2" ;
				unshift(@new,$wk);
			}
		}	else	{
			push(@new,"$_"); 								#<<<そのまま出力
		}
		$cnt++ ;
	}
	if ( $found == 0 ) {	&fileunlock ;	&error("ストッピする記事Noが見つかりませんでした") ;	}

	if ( !(open(OUT,">$logfile")))	{	&fileunlock ;	&error("ログファイル($logfile)のオープンに失敗しました");	}
	print OUT @new;
	close(OUT);
	&fileunlock ;	#ファイルロック解除

	#COOKIE設定
	&cookieset if ( $FORM{'proc'} ne 'delete' );

	if ( $damedame == 0 )	{
		print "Location: $script?\n\n";
	}	else	{
		print "Content-type: text/html\n\n";
		print "<html><head><META HTTP-EQUIV=\"Refresh\" CONTENT=\"0; URL=";
		print "$script\"></head><body></body></html>\n\n";
	}

}
###<-------------------------------------------------------------
###<---   クッキー取得
###<--------------------------------------------------------------
sub cookieget	{
	$cookies = $ENV{'HTTP_COOKIE'};
	@pairs = split(/;/,$cookies);
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$name =~ s/ //g;
		$DUMMY{$name} = $value;
	}
	@pairs = split(/,/,$DUMMY{'kakikomitai'});
	foreach $pair (@pairs) {
		($name, $value) = split(/\!/, $pair);
		$COOKIE{$name} = $value;
	}
}
###<-------------------------------------------------------------
###<---   クッキー設定
###<--------------------------------------------------------------
sub cookieset {
	($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg)
		=gmtime(time + 30*24*60*60);
	$yearg  += 1900 ;
	if ($secg  < 10)  { $secg  = "0$secg";  }
	if ($ming  < 10)  { $ming  = "0$ming";  }
	if ($hourg < 10)  { $hourg = "0$hourg"; }
	if ($mdayg < 10)  { $mdayg = "0$mdayg"; }
	$mong = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[$mong];
	$youbi = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')[$wdayg];
	$date_gmt = "$youbi, $mdayg\-$mong\-$yearg $hourg:$ming:$secg GMT";
	$cook="nm\!$FORM{'name'},em\!$FORM{'email'},hp\!$FORM{'hp'},cl\!$FORM{'color'},ps\!$FORM{'pass'}";
	print "Set-Cookie: kakikomitai=$cook; expires=$date_gmt\n";
}
###<--------------------------------------------------------------
###<---   エラー処理
###<--------------------------------------------------------------
sub error {
	&header ;
	print "<br><br><br><font color=\"$tcolor\">$_[0]</font><br><br><br>\n";
	&footer;
	exit;
}
###<-------------------------------------------------------------
###<---   パスワード暗号化
###<--------------------------------------------------------------
sub pass_enc {
	if ( $ango == 1 ) {
		$pass = crypt($_[0], $_[0]);
	}	else	{
		$pass = $_[0];
	}
}
###<-------------------------------------------------------------
###<---   パスワードチェック
###<--------------------------------------------------------------
sub pass_dec {
	if ( $ango == 1 ) {
		if ($_[0] ne '' && ( crypt($FORM{'pass'}, $_[0]) eq $_[0]) )  {
			return 0 ;
		}
	}	else	{
		if ($FORM{'pass'} eq $_[0]) {
			return 0 ;
		}
	}
	return 1;
}
###<--------------------------------------------------------------
###<---   ファイルロック設定
###<--------------------------------------------------------------
sub filelock {
	foreach (1 .. 5) {
		if (-e $lockfile) { sleep(1); }
		else {
			open(LOCK,">$lockfile");
			close(LOCK);
			return;
		}
	}
	&error("只今他の方が書き込み中です。ブラウザの「戻る」で戻って再度登録を行って下さい。<br>又はロックファイル($lockfile)が残ったままかもしれませんので、同ファイルを削除して下さい。");
}
###<--------------------------------------------------------------
###<---   ファイルロック解除
###<--------------------------------------------------------------
sub fileunlock {
	if (-e $lockfile) { unlink($lockfile); }
}
###<--------------------------------------------------------------
###<---   SendMail
###<--------------------------------------------------------------
sub SMail {
	$ttl = $title;
	if ( $FORM{'email'} ) { $email = $FORM{'email'} ; } else { $email = $smail_address ; }
	if ( $hiho == 1 )	{
	   	&jcode'convert(*ttl,'euc');
		open(MAIL,"| $sendmail -s \"$ttl\" -f $email $smail_address ") || &error("Sendmail Error!!");
	}	else	{
		open(MAIL,"| $sendmail -t") || &error("Sendmail Error!!");
		$mailbuf = "To: $smail_address\n";
		$mailbuf .= "Reply-to: $email\n";
		$mailbuf .= "Subject: $ttl\n";
		$mailbuf .= "Content-Transfer-Encoding: 7bit\n";
		$mailbuf .= "Content-type: text/plain\n";
		$mailbuf .= "\n\n";
	}
	$mailbuf .= "============================================================\n";
	$mailbuf .= "■---『$title』に投稿がありました---■\n\n";
	$mailbuf .= "投稿日時：$today\n";
	$mailbuf .= "投稿者のお名前：$FORM{'name'}\n";
	$mailbuf .= "投稿者のメールアドレス：$FORM{'email'}\n";
	if ($FORM{'hp'} ne "") { $mailbuf .=  "投稿者のホームページ：http://$FORM{'hp'}\n"; }
	$mailbuf .= "============================================================\n\n";
	$mailbuf .= "■タイトル\n";
	if ($FORM{'resno'} ne "") { $mailbuf .= "「$sv_title」についての返信です\n\n"; }
	elsif ($FORM{'resno'} eq "" && $FORM{'title'} eq "") { $mailbuf .= "（無題）\n\n"; }
	else	{ $mailbuf .= "$FORM{'title'}\n\n" ;	}
	$mailbuf .= "■コメント\n";
	$mailbuf .= "$FORM{$name_comment}\n\n";
	$mailbuf .= "============================================================\n";
	#漢字コードＪＩＳ変換＆改行コードLF変換。
	$mailbuf	=~ s/\r\n/\n/g;		$mailbuf	=~ s/\r/\n/g;	$mailbuf	=~ s/<br>/\n/g;
	$mailbuf =~ s/&amp;/&/g;	$mailbuf =~ s/&quot;/"/g;
	$mailbuf =~ s/&lt;/</g;	$mailbuf =~ s/&gt;/>/g;
   	&jcode'convert(*mailbuf,'jis');
	print MAIL	$mailbuf ;
	close(MAIL);
}
