Summary:	Courier-IMAP server
Name:		courier-imap
Version:	1.3.8.2
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
URL:		http://www.inter7.com/courierimap/
Source0:	http://download.sourceforge.net/courier/%{name}-%{version}.tar.gz 
Source1:	%{name}.init
Source2:	%{name}-pop3.init
Source3:	%{name}-authdaemon.init
Source4:	%{name}.pamd
Source5:	%{name}-pop3.pamd
Source6:	%{name}.sysconfig
Source7:	%{name}-pop3.sysconfig
Source8:	%{name}-authdaemon.sysconfig
Requires:	%{name}-common = %{version}
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
Prereq:		rc-scripts
Provides:	imapdaemon
Obsoletes:	imapdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	/usr/lib/courier-imap
%define		_sysconfdir	/etc/courier-imap

%description
Courier-IMAP is an IMAP server for Maildir mailboxes.

%description -l pl
Courier-IMAP jest serwerem IMAP dla skrzynek pocztowych Maildir.

%package common
Summary:	Common files for imap and pop daemons.
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Prereq:		rc-scripts

%description common
Common files for imap and pop daemons.

%description -l pl common
Pliki wspólne dla serwerów imap i pop.

%package pop3
Summary:	Courier-IMAP POP3 Server
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Requires:	%{name}-common = %{version}
Prereq:		rc-scripts
Provides:	pop3daemon
Obsoletes:	pop3daemon

%description pop3
Courier-IMAP POP3 is an POP3 server for Maildir mailboxes.

%description -l pl pop3
Courier-IMAP POP3 jest serwerem POP3 dla skrzynek pocztowych Maildir.

%prep
%setup -q

%build
%configure2_13 \
	--with-authdaemonvar=/var/lib/authdaemon
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{pam.d,rc.d/init.d,security,sysconfig} \
	$RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/courier-imap
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/courier-imap-pop3
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/authdaemon

install %{SOURCE4} $RPM_BUILD_ROOT/etc/pam.d/imap
install %{SOURCE5} $RPM_BUILD_ROOT/etc/pam.d/pop3

install %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/courier-imap
install %{SOURCE7} $RPM_BUILD_ROOT/etc/sysconfig/courier-imap-pop3
install %{SOURCE8} $RPM_BUILD_ROOT/etc/sysconfig/authdaemon

rm -rf  $RPM_BUILD_ROOT%{_mandir}/man8/{authcram,authpam,authpwd,authshadow,authuserdb,authvchkpw,pw2userdb,vchkpw2userdb,authdaemon,authdaemond,authldap,authmysql}.8 \
	$RPM_BUILD_ROOT%{_sbindir}/{*db,mk*cert}

mv -f imap/README README.imap
mv -f maildir/README.maildirquota.txt README.maildirquota

install authlib/authdaemonrc		$RPM_BUILD_ROOT%{_sysconfdir}
install authlib/authldaprc		$RPM_BUILD_ROOT%{_sysconfdir}
install authlib/authmysqlrc		$RPM_BUILD_ROOT%{_sysconfdir}

mv -f $RPM_BUILD_ROOT%{_datadir}/*db \
	$RPM_BUILD_ROOT%{_sbindir}
mv -f $RPM_BUILD_ROOT%{_datadir}/mk*cert \
	$RPM_BUILD_ROOT%{_sbindir}

echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authcram.8
echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authpam.8
echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authpwd.8
echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authshadow.8
echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authuserdb.8
echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authvchkpw.8
echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authdaemon.8
echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authdaemond.8
echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authmysql.8
echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authldap.8
echo ".so makeuserdb.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/pw2userdb.8
echo ".so makeuserdb.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/vchkpw2userdb.8

gzip -9nf README* imap/BUGS AUTHORS COPYING

touch $RPM_BUILD_ROOT/etc/security/blacklist.{pop3,imap}

%post
DESC="%{name} daemon"; %chkconfig_add

%preun
%chkconfig_del

%post common
NAME=authdaemon; DESC="%{name} authdaemon"; %chkconfig_add

%preun common
NAME=authdaemon; %chkconfig_del

%post pop3
NAME=%{name}-pop3; DESC="%{name} pop3 daemon; %chkconfig_add

%preun pop3
NAME=%{name}-pop3; %chkconfig_del

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config %verify(not size mtime md5) /etc/pam.d/imap
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.imap
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/courier-imap
%attr(754,root,root) /etc/rc.d/init.d/courier-imap
%{_sysconfdir}/imapd.cnf
%attr(755,root,root) %{_bindir}/imapd
%attr(755,root,root) %{_sbindir}/imaplogin
%attr(755,root,root) %{_sbindir}/mkimapdcert

%files common
%defattr(644,root,root,755)
%doc *.gz imap/*.gz
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/authdaemon
%attr(754,root,root) /etc/rc.d/init.d/authdaemon
%attr(750,root,root) %dir %{_sysconfdir}
%dir %{_libexecdir}
%dir %{_libexecdir}/authlib
%{_sysconfdir}/authdaemonrc
%{_sysconfdir}/authldaprc
%{_sysconfdir}/authmysqlrc
%{_sysconfdir}/quotawarnmsg.example
%attr(755,root,root) %{_bindir}/couriertls
%attr(755,root,root) %{_bindir}/maildirmake
%attr(755,root,root) %{_sbindir}/makeuserdb
%attr(755,root,root) %{_sbindir}/pw2userdb
%attr(755,root,root) %{_sbindir}/userdb
%attr(755,root,root) %{_sbindir}/userdbpw
%attr(755,root,root) %{_sbindir}/vchkpw2userdb
%attr(755,root,root) %{_libexecdir}/authlib/authdaemon
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.*
%attr(755,root,root) %{_libexecdir}/couriertcpd
%attr(755,root,root) %{_libexecdir}/deliverquota
%attr(755,root,root) %{_libexecdir}/logger
%attr(755,root,root) %{_libexecdir}/makedatprog
%{_mandir}/man*/*

%files pop3
%defattr(644,root,root,755)
%attr(640,root,root) %config %verify(not size mtime md5) /etc/pam.d/pop3
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.pop3
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/courier-imap-pop3
%attr(754,root,root) /etc/rc.d/init.d/courier-imap-pop3
%attr(755,root,root) %{_bindir}/pop3d
%attr(755,root,root) %{_sbindir}/mkpop3dcert
%attr(755,root,root) %{_sbindir}/pop3login
%{_sysconfdir}/pop3d.cnf
