# TODO:
# - put imap-ssl and pop3-ssl to separate packages - some want to have
#   ssl-only system (or non-ssl only system)
#   see also http://thread.gmane.org/gmane.linux.pld.devel.english/2509/focus=2509
# - fix manpages:
#    [set $man.base.url.for.relative.links]/maildirquota.html
#
# Conditional build:
%bcond_with	toplevel	# Allow toplevel folders. More info: http://www.ricky-chan.co.uk/courier/

Summary:	Courier-IMAP server
Summary(pl.UTF-8):	Serwer Courier-IMAP
Name:		courier-imap
Version:	4.10.0
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://downloads.sourceforge.net/courier/%{name}-%{version}.tar.bz2
# Source0-md5:	2f95c99b9ad1380b9f3ac733ccd741a2
Source1:	%{name}.init
Source2:	%{name}-ssl.init
Source3:	%{name}-pop3.init
Source4:	%{name}-pop3-ssl.init
Source5:	%{name}.pamd
Source6:	%{name}-pop3.pamd
Patch0:		%{name}-dirs.patch
Patch1:		%{name}-certsdir.patch
Patch2:		%{name}-maildir.patch
Patch3:		%{name}-toplevel.patch
Patch4:		%{name}-drop-makedat.patch
URL:		http://www.courier-mta.org/imap/
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake
BuildRequires:	courier-authlib-devel >= 0.61
BuildRequires:	db-devel
BuildRequires:	gdbm-devel
BuildRequires:	gnet-devel
BuildRequires:	libidn-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pkgconfig
BuildRequires:	procps
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	sysconftool
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}-%{release}
Requires:	/sbin/chkconfig
Requires:	pam >= 0.79.0
Requires:	rc-scripts
Provides:	imapdaemon
Obsoletes:	imapdaemon
Conflicts:	cyrus-imapd
Conflicts:	imap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	/usr/%{_lib}/courier-imap
%define		_sysconfdir	/etc/courier-imap
%define		_certsdir	%{_sysconfdir}/certs
%define		_localstatedir	/var/spool/courier-imap

%description
Courier-IMAP is an IMAP server for Maildir mailboxes.

%description -l pl.UTF-8
Courier-IMAP jest serwerem IMAP dla skrzynek pocztowych Maildir.

%package common
Summary:	Common files for imap and pop3 daemons
Summary(pl.UTF-8):	Pliki wspólne dla serwerów imap i pop3
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	/sbin/chkconfig
Requires:	courier-authlib
Requires:	procps
Requires:	rc-scripts

%description common
Common files for imap and pop3 daemons.

%description common -l pl.UTF-8
Pliki wspólne dla serwerów imap i pop3.

%package deliverquota
Summary:	Deliver to a Maildir with a quota
Summary(pl.UTF-8):	Obsługa quoty przy dostarczaniu poczty do skrzynek Maildir
Group:		Networking/Daemons

%description deliverquota
deliverquota is a temporary hack to implement E-mail delivery to a
Maildir with a software-imposed quota.

%description deliverquota -l pl.UTF-8
deliverquota jest tymczasowym rozwiązaniem implementującym
dostarczanie e-maili do skrzynek Maildir z programowo narzuconą quotą.

%package maildirmake
Summary:	Tool for making mail folders in Maildir format
Summary(pl.UTF-8):	Narzędzie do tworzenia folderów w formacie Maildir
Group:		Networking/Daemons
Conflicts:	qmail-maildirmake

%description maildirmake
Maildirmake is a tool for making mail folders in Maildir format.

%description maildirmake -l pl.UTF-8
Maildirmake jest narzędziem do tworzenia folderów pocztowych w
formacie Maildir.

%package pop3
Summary:	Courier-IMAP POP3 Server
Summary(pl.UTF-8):	Serwer Courier-IMAP POP3
Group:		Networking/Daemons/POP3
Requires:	%{name}-common = %{version}-%{release}
Requires:	pam >= 0.79.0
Provides:	pop3daemon
Obsoletes:	pop3daemon
Conflicts:	cyrus-imapd
Conflicts:	imap-pop3
Conflicts:	solid-pop3d
Conflicts:	tpop3d

%description pop3
Courier-IMAP POP3 is an POP3 server for Maildir mailboxes.

%description pop3 -l pl.UTF-8
Courier-IMAP POP3 jest serwerem POP3 dla skrzynek pocztowych Maildir.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%if %{with toplevel}
%patch3 -p1
%endif
%patch4 -p1

install %{SOURCE1} courier-imap.in
install %{SOURCE2} courier-imap-ssl.in
install %{SOURCE3} courier-pop3.in
install %{SOURCE4} courier-pop3-ssl.in
rm -f makedat/configure.in

%build
# Change Makefile.am files and force recreate Makefile.in's.
find -type f -a '(' -name configure.in -o -name configure.ac ')' | while read FILE; do
	cd "$(dirname "$FILE")"

	if [ -f Makefile.am ]; then
		%{__sed} -i -e '/_[L]DFLAGS=-static/d' Makefile.am
	fi

	%{__libtoolize}
	%{__aclocal}
	%{__autoconf}
	if grep -q AC_CONFIG_HEADER configure.in; then
		%{__autoheader}
	fi
	%{__automake}

	cd -
done

%configure \
	--with-db=db \
	--enable-unicode \
	--with-authchangepwdir=/var/tmp \
	--with-certsdir=%{_certsdir} \
	--with-mailer=/usr/lib/sendmail

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{pam.d,rc.d/init.d,security},%{_certsdir}}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install -p courier-imap $RPM_BUILD_ROOT/etc/rc.d/init.d/courier-imap
install -p courier-imap-ssl $RPM_BUILD_ROOT/etc/rc.d/init.d/courier-imap-ssl
install -p courier-pop3 $RPM_BUILD_ROOT/etc/rc.d/init.d/courier-pop3
install -p courier-pop3-ssl $RPM_BUILD_ROOT/etc/rc.d/init.d/courier-pop3-ssl
cp -a %{SOURCE5} $RPM_BUILD_ROOT/etc/pam.d/imap
cp -a %{SOURCE6} $RPM_BUILD_ROOT/etc/pam.d/pop3

rm -rf $RPM_BUILD_ROOT%{_sbindir}/mk*cert

cp -af imap/README README.imap
cp -af imap/ChangeLog ChangeLog
cp -af maildir/README.maildirquota.txt README.maildirquota

mv -f $RPM_BUILD_ROOT%{_datadir}/mk*cert $RPM_BUILD_ROOT%{_sbindir}

cp -a tcpd/couriertls.1 $RPM_BUILD_ROOT%{_mandir}/man8/couriertls.8
cp -a imap/courierpop3d.8 $RPM_BUILD_ROOT%{_mandir}/man8/courierpop3d.8

touch $RPM_BUILD_ROOT/etc/security/blacklist.{pop3,imap}
touch $RPM_BUILD_ROOT%{_sysconfdir}/shared/index

# make config files
./sysconftool $RPM_BUILD_ROOT%{_sysconfdir}/*.dist

# set yes to start imapd and pop3d
sed -i 's/^POP3DSTART.*/POP3DSTART=YES/' $RPM_BUILD_ROOT%{_sysconfdir}/pop3d
sed -i 's/^IMAPDSTART.*/IMAPDSTART=YES/' $RPM_BUILD_ROOT%{_sysconfdir}/imapd

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/*.dist

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add courier-imap
/sbin/chkconfig --add courier-imap-ssl
%service courier-imap restart "courier-imap daemon"
%service courier-imap-ssl restart "courier-imap-ssl daemon"

%preun
if [ "$1" = "0" ]; then
	%service courier-imap stop
	/sbin/chkconfig --del courier-imap
fi

if [ "$1" = "0" ]; then
	%service courier-imap-ssl stop
	/sbin/chkconfig --del courier-imap-ssl
fi


%triggerin -- %{name} < 3.0.5
if [ -f /var/lib/openssl/certs/imapd.pem ]; then
	echo
	echo imapd.pem has been moved automatically to %{_certsdir}
	echo
	mv -f /var/lib/openssl/certs/imapd.pem %{_certsdir}
fi
if [ -f /etc/sysconfig/courier-imap ]; then
	. /etc/sysconfig/courier-imap
	for opt in `grep ^[^#] /etc/sysconfig/courier-imap |grep -v TLS_CERTFILE |grep -v MAILDIR |grep -v COURIERTLS |cut -d= -f1`;
	do
		eval opt2=\$$opt
		sed -i s/^$opt=.*/"$opt=\"$opt2\""/ %{_sysconfdir}/imapd
		sed -i s/^$opt=.*/"$opt=\"$opt2\""/ %{_sysconfdir}/imapd-ssl
	done
	sed -i s/^SSLADDRESS=.*/"SSLADDRESS=$ADDRESS_SSL"/ %{_sysconfdir}/imapd-ssl
	sed -i s/^SSLPORT=.*/"SSLPORT=$PORTS_SSL"/ %{_sysconfdir}/imapd-ssl
	sed -i s!^MAILDIRPATH=.*!"MAILDIRPATH=\"$MAILDIR\""! %{_sysconfdir}/imapd-ssl
	sed -i s!^MAILDIRPATH=.*!"MAILDIRPATH=\"$MAILDIR\""! %{_sysconfdir}/imapd
	echo
	echo IMAPD config file has been rewriten to %{_sysconfdir}/imapd,imapd-ssl
	echo please look at them
	echo
fi
%service -q courier-imap restart

%triggerin -- %{name} < 3.0.6
. %{_sysconfdir}/imapd-ssl
if [ $TLS_CACHEFILE = "/var/couriersslcache" ]; then
	sed -i s/^TLS_CACHEFILE=.*/"TLS_CACHEFILE=\/var\/spool\/courier-imap\/couriersslcache"/ %{_sysconfdir}/imapd-ssl
fi

%triggerin -n %{name}-common -- %{name}-userdb
echo
echo courier-imap-userdb is obsolete
echo install courier-authlib-userdb package
echo

%triggerin -n %{name}-common -- %{name}-common < 3.0.5
/sbin/chkconfig --del authdaemon
if [ -f /var/lock/subsys/authdaemon ]; then
	kill `cat /var/lib/authdaemon/pid`
	rm -f /var/lock/subsys/authdaemon
fi
if [ -f /etc/sysconfig/authdaemon ]; then
	. /etc/sysconfig/authdaemon
	sed -i s/^version.*/version=authdaemond.$METHOD/ %{_sysconfdir}/authdaemonrc
fi
echo
echo Changes to version 3.0.5 :
echo - config files has been splited and moved to %{_sysconfdir}
echo - certificates directory has changed to %{_certsdir}
echo

%post pop3
/sbin/chkconfig --add courier-pop3
/sbin/chkconfig --add courier-pop3-ssl
/sbin/chkconfig --del courier-imap-pop3 >/dev/null 2>&1 || :
if [ -f /var/lock/subsys/courier-imap-pop3 ]; then
	/sbin/service courier-imap-pop3 stop >&2
	/sbin/service courier-pop3 start >&2
else
	%service courier-pop3 restart "courier-pop3 daemon"
fi
%service courier-pop3-ssl restart "courier-pop3-ssl daemon"

%preun pop3
if [ "$1" = "0" ]; then
	%service courier-pop3 stop
	/sbin/chkconfig --del courier-pop3
	%service courier-pop3-ssl stop
	/sbin/chkconfig --del courier-pop3-ssl
fi

%triggerin -n %{name}-pop3 -- %{name}-pop3 < 3.0.5
if [ -f /var/lib/openssl/certs/pop3d.pem ]; then
	echo
	echo pop3d.pem has been moved automatically to %{_certsdir}
	echo
	mv -f /var/lib/openssl/certs/pop3d.pem %{_certsdir}
fi
if [ -f /etc/sysconfig/courier-pop3 ]; then
	. /etc/sysconfig/courier-pop3
	for opt in `grep ^[^#] /etc/sysconfig/courier-pop3 |grep -v TLS_CERTFILE |grep -v MAILDIR |grep -v COURIERTLS |cut -d= -f1`;
	do
		eval opt2=\$$opt
		sed -i s/^$opt=.*/"$opt=\"$opt2\""/ %{_sysconfdir}/pop3d
		sed -i s/^$opt=.*/"$opt=\"$opt2\""/ %{_sysconfdir}/pop3d-ssl
	done
	sed -i s!^MAILDIRPATH=.*!"MAILDIRPATH=\"$MAILDIR\""! %{_sysconfdir}/pop3d-ssl
	sed -i s!^MAILDIRPATH=.*!"MAILDIRPATH=\"$MAILDIR\""! %{_sysconfdir}/pop3d
	echo
	echo POP3D config file has been rewriten to %{_sysconfdir}/{pop3d,pop3d-ssl}
	echo please look at them
	echo
fi
%service courier-pop3 restart

%triggerin -n %{name}-pop3 -- %{name}-pop3 < 3.0.6
. %{_sysconfdir}/pop3d-ssl
if [ $TLS_CACHEFILE = "/var/couriersslcache" ]; then
	sed -i s/^TLS_CACHEFILE=.*/"TLS_CACHEFILE=\/var\/spool\/courier-imap\/couriersslcache"/ %{_sysconfdir}/pop3d-ssl
fi

%files
%defattr(644,root,root,755)
%doc maildir/README.sharedfolders.txt imap/README.proxy tcpd/README.couriertls
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/imap
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.imap
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/imapd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/imapd-ssl
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/imapd.cnf
%attr(754,root,root) /etc/rc.d/init.d/courier-imap
%attr(754,root,root) /etc/rc.d/init.d/courier-imap-ssl
%attr(755,daemon,daemon) %dir %{_sysconfdir}/shared
%attr(755,daemon,daemon) %dir %{_sysconfdir}/shared.tmp
%attr(644,daemon,daemon) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/shared/index
%attr(755,root,root) %{_bindir}/imapd
%attr(755,root,root) %{_bindir}/maildiracl
%attr(755,root,root) %{_bindir}/maildirkw
%attr(755,root,root) %{_sbindir}/imaplogin
%attr(755,root,root) %{_sbindir}/mkimapdcert
%attr(755,root,root) %{_sbindir}/sharedindexinstall
%attr(755,root,root) %{_sbindir}/sharedindexsplit
%attr(755,root,root) %{_libexecdir}/imapd.rc
%attr(755,root,root) %{_libexecdir}/imapd-ssl.rc
%{_mandir}/man8/imapd*
%{_mandir}/man1/maildiracl.1*
%{_mandir}/man1/maildirkw.1*

%files common
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog imap/BUGS INSTALL README*
%attr(751,root,root) %dir %{_sysconfdir}
%attr(750,root,root) %dir %{_certsdir}
%attr(770,daemon,daemon) %dir %{_localstatedir}
%dir %{_libexecdir}
%{_sysconfdir}/quotawarnmsg.example
%attr(755,root,root) %{_bindir}/couriertls
%attr(755,root,root) %{_libexecdir}/couriertcpd
%{_mandir}/man1/couriert*
%{_mandir}/man8/couriert*
%{_mandir}/man8/mk*

%files deliverquota
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/deliverquota
%{_mandir}/man8/deliverquota*

%files maildirmake
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/maildirmake
%{_mandir}/man1/maildirmake*

%files pop3
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/pop3
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.pop3
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pop3d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pop3d-ssl
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pop3d.cnf
%attr(754,root,root) /etc/rc.d/init.d/courier-pop3
%attr(754,root,root) /etc/rc.d/init.d/courier-pop3-ssl
%attr(755,root,root) %{_bindir}/pop3d
%attr(755,root,root) %{_sbindir}/mkpop3dcert
%attr(755,root,root) %{_sbindir}/pop3login
%attr(755,root,root) %{_libexecdir}/pop3d.rc
%attr(755,root,root) %{_libexecdir}/pop3d-ssl.rc
%{_mandir}/man8/courierpop*
