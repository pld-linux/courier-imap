#
# Conditional build:
# _without_ldap - without LDAP support
# _without_mysql - without MySQL support
# _without_pgsql - without PostgreSQL support
Summary:	Courier-IMAP server
Summary(pl):	Serwer Courier-IMAP
Name:		courier-imap
Version:	1.5.3
Release:	7
License:	GPL
Group:		Networking/Daemons
Source0:	http://download.sourceforge.net/courier/%{name}-%{version}.tar.gz
# Source0-md5:	132c2405e3857b3fa2a6369d77e19fd9
Source1:	%{name}.init
Source2:	%{name}-pop3.init
Source3:	%{name}-authdaemon.init
Source4:	%{name}.pamd
Source5:	%{name}-pop3.pamd
Source6:	%{name}.sysconfig
Source7:	%{name}-pop3.sysconfig
Source8:	%{name}-authdaemon.sysconfig
Patch0:		ftp://ftp.pld-linux.org/people/siefca/patches/courier/%{name}-%{version}-myownquery.patch
URL:		http://www.inter7.com/courierimap/
%{!?_without_pgsql:BuildRequires:	postgresql-devel}
%{!?_without_mysql:BuildRequires:	mysql-devel}
%{!?_without_mysql:BuildRequires:	zlib-devel}
%{!?_without_ldap:BuildRequires:	openldap-devel}
BuildRequires:	gdbm-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
PreReq:		%{name}-common = %{version}
Provides:	imapdaemon
Obsoletes:	imapdaemon
Conflicts:	cyrus-imapd
Conflicts:	imap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	/usr/lib/courier-imap
%define		_sysconfdir	/etc/courier-imap

%description
Courier-IMAP is an IMAP server for Maildir mailboxes.

%description -l pl
Courier-IMAP jest serwerem IMAP dla skrzynek pocztowych Maildir.

%package common
Summary:	Common files for imap and pop daemons
Summary(pl):	Pliki wspólne dla serwerów imap i pop
Group:		Networking/Daemons
PreReq:		rc-scripts
PreReq:		/sbin/chkconfig
Requires:	%{name}-maildirmake
Requires:	%{name}-deliverquota
Requires:	%{name}-userdb

%description common
Common files for imap and pop daemons.

%description common -l pl
Pliki wspólne dla serwerów imap i pop.

%package userdb
Summary:	Commands used to create the /etc/userdb.dat
Summary(pl):	Polecenia do tworzenia /etc/userdb.dat
Group:		Networking/Daemons

%description userdb
Commands used to create the /etc/userdb.dat.

%description userdb -l pl
Polecenia u¿ywane do stworzenia /etc/userdb.dat.

%package deliverquota
Summary:	Deliver to a Maildir with a quota
Summary(pl):	Obs³uga quoty przy dostarczaniu poczty do skrzynek Maildir
Group:		Networking/Daemons

%description deliverquota
deliverquota is a temporary hack to implement E-mail delivery to a
Maildir with a software-imposed quota.

%description deliverquota -l pl
deliverquota jest tymczasowym rozwi±zaniem implementuj±cym
dostarczanie e-maili do skrzynek Maildir z programowo narzucon± quot±.

%package maildirmake
Summary:	Tool for making mail folders in Maildir format
Summary(pl):	Narzêdzie do tworzenia folderów w formacie Maildir
Group:		Networking/Daemons
Conflicts:	qmail-maildirmake

%description maildirmake
Maildirmake is a tool for making mail folders in Maildir format.

%description maildirmake -l pl
Maildirmake jest narzêdziem do tworzenia folderów pocztowych w
formacie Maildir.

%package pop3
Summary:	Courier-IMAP POP3 Server
Summary(pl):	Serwer Courier-IMAP POP3
Group:		Networking/Daemons
PreReq:		%{name}-common = %{version}
Provides:	pop3daemon
Obsoletes:	pop3daemon
Conflicts:	cyrus-imapd
Conflicts:	imap-pop3
Conflicts:	tpop3d
Conflicts:	solid-pop3d

%description pop3
Courier-IMAP POP3 is an POP3 server for Maildir mailboxes.

%description pop3 -l pl
Courier-IMAP POP3 jest serwerem POP3 dla skrzynek pocztowych Maildir.

%package authldap
Summary:	LDAP authentication daemon for Courier IMAP
Summary(pl):	Demon autentykacji LDAP do Courier IMAP
Group:		Networking/Daemons
PreReq:		%{name}-common = %{version}

%description authldap
This package provides LDAP authentication for Courier IMAP.

%description authldap -l pl
Ten pakiet pozwala na korzystanie z autentykacji LDAP w Courier IMAP.

%package authmysql
Summary:	MySQL authentication daemon for Courier IMAP
Summary(pl):	Demon autentykacji MySQL do Courier IMAP
Group:		Networking/Daemons
PreReq:		%{name}-common = %{version}
Requires:	zlib

%description authmysql
This package provides MySQL authentication for Courier IMAP.

%description authmysql -l pl
Ten pakiet pozwala na korzystanie z autentykacji MySQL w Courier IMAP.

%package authpgsql
Summary:	PostgreSQL authentication daemon for Courier IMAP
Summary(pl):	Demon autentykacji PostgreSQL do Courier IMAP
Group:		Networking/Daemons
PreReq:		%{name}-common = %{version}

%description authpgsql
This package provides PostgreSQL authentication for Courier IMAP.

%description authpgsql -l pl
Ten pakiet pozwala na korzystanie z autentykacji PostgreSQL w Courier
IMAP.

%prep
%setup -q
%patch0 -p1

%build
%configure2_13 \
	--enable-unicode \
	--with-authchangepwdir=/var/tmp \
	--with-authdaemonvar=/var/lib/authdaemon \
	%{!?_without_mysql:--with-mysql-libs=%{_libdir} --with-mysql-includes=%{_includedir}/mysql} \
	%{?_without_mysql:--without-authmysql} \
	%{!?_without_pgsql:--with-pgsql-libs=%{_libdir} --with-pgsql-includes=%{_includedir}/postgresql} \
	%{?_without_pgsql:--without-authpgsql} \
	%{?_without_ldap:--without-authldap}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{pam.d,rc.d/init.d,security,sysconfig} \
	$RPM_BUILD_ROOT{%{_sysconfdir},/var/lib/authdaemon}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/courier-imap
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/courier-pop3
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/authdaemon

install %{SOURCE4} $RPM_BUILD_ROOT/etc/pam.d/imap
install %{SOURCE5} $RPM_BUILD_ROOT/etc/pam.d/pop3

install %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/courier-imap
install %{SOURCE7} $RPM_BUILD_ROOT/etc/sysconfig/courier-pop3
install %{SOURCE8} $RPM_BUILD_ROOT/etc/sysconfig/authdaemon

rm -rf	$RPM_BUILD_ROOT%{_mandir}/man8/{authcram,authpam,authpwd,authshadow,authuserdb,authvchkpw,pw2userdb,vchkpw2userdb,authdaemon,authdaemond,authldap,authmysql}.8 \
	$RPM_BUILD_ROOT%{_sbindir}/{*db,mk*cert}

mv -f authlib/README.authmysql.html README.authmysql.html
mv -f authlib/README.ldap README.ldap
mv -f authlib/README.authmysql.myownquery README.authmysql.myownquery
mv -f imap/README README.imap
mv -f imap/ChangeLog ChangeLog
mv -f maildir/README.maildirquota.txt README.maildirquota

install authlib/authdaemonrc		$RPM_BUILD_ROOT%{_sysconfdir}
install authlib/authldaprc		$RPM_BUILD_ROOT%{_sysconfdir}
install authlib/authmysqlrc		$RPM_BUILD_ROOT%{_sysconfdir}
install authlib/authpgsqlrc		$RPM_BUILD_ROOT%{_sysconfdir}

mv -f $RPM_BUILD_ROOT%{_datadir}/*db \
	$RPM_BUILD_ROOT%{_sbindir}
mv -f $RPM_BUILD_ROOT%{_datadir}/mk*cert \
	$RPM_BUILD_ROOT%{_sbindir}

mv -f tcpd/couriertls.1 $RPM_BUILD_ROOT%{_mandir}/man8/couriertls.8
mv -f imap/courierpop3d.8 $RPM_BUILD_ROOT%{_mandir}/man8/courierpop3d.8

echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authcram.8
echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authpam.8
echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authpwd.8
echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authshadow.8
echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authuserdb.8
echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authvchkpw.8
echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authdaemon.8
echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authdaemond.8
%{!?_without_pgsql:echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authpgsql.8}
%{!?_without_mysql:echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authmysql.8}
%{!?_without_ldap:echo ".so authlib.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/authldap.8}
echo ".so makeuserdb.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/pw2userdb.8
echo ".so makeuserdb.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/vchkpw2userdb.8

touch $RPM_BUILD_ROOT/etc/security/blacklist.{pop3,imap}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add courier-imap

if [ -f /var/lock/subsys/courier-imap ]; then
	/etc/rc.d/init.d/courier-imap restart >&2
else
	echo "Run \"/etc/rc.d/init.d/courier-imap start\" to start courier-imap daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/courier-imap ]; then
		/etc/rc.d/init.d/courier-imap stop >&2
	fi
	/sbin/chkconfig --del courier-imap
fi

%post common
/sbin/chkconfig --add authdaemon

if [ -f /var/lock/subsys/authdaemon ]; then
	/etc/rc.d/init.d/authdaemon restart >&2
else
	echo "Run \"/etc/rc.d/init.d/authdaemon start\" to start courier-imap authdaemon."
fi

%preun common
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/authdaemon ]; then
		/etc/rc.d/init.d/authdaemon stop >&2
	fi

	/sbin/chkconfig --del authdaemon
fi

%post pop3
/sbin/chkconfig --add courier-pop3
/sbin/chkconfig --del courier-imap-pop3 2>&1 >/dev/null
if [ -f /var/lock/subsys/courier-imap-pop3 ]; then
	/etc/rc.d/init.d/courier-imap-pop3 stop >&2
	/etc/rc.d/init.d/courier-pop3 start >&2
elif [ -f /var/lock/subsys/courier-pop3 ]; then
	/etc/rc.d/init.d/courier-pop3 restart >&2
else
	echo "Run \"/etc/rc.d/init.d/courier-pop3 start\" to start courier-pop3 daemon."
fi
rm -f /etc/rc.d/init.d/courier-imap-pop3

%preun pop3
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/courier-pop3 ]; then
		/etc/rc.d/init.d/courier-pop3 stop >&2
	fi
	/sbin/chkconfig --del courier-pop3
	if [ -f /var/lock/subsys/courier-imap-pop3 ]; then
		/etc/rc.d/init.d/courier-imap-pop3 stop >&2
	fi
	/sbin/chkconfig --del courier-imap-pop3 2>&1 >/dev/null
	rm -f /etc/rc.d/init.d/courier-imap-pop3
fi

%post authldap
METHOD=plain
. /etc/sysconfig/authdaemon
if [ "$METHOD" = "ldap" ]; then
	if [ -f /var/lock/subsys/authdaemon ]; then
		/etc/rc.d/init.d/authdaemon restart >&2
	else
		echo "Run \"/etc/rc.d/init.d/authdaemon start\" to start courier-imap authdaemon."
	fi
fi

%preun authldap
METHOD=plain
. /etc/sysconfig/authdaemon
if [ "$1" = "$0" -a "$METHOD" = "ldap" ]; then
	if [ -f /var/lock/subsys/authdaemon ]; then
		/etc/rc.d/init.d/authdaemon stop >&2
	fi
fi

%post authmysql
METHOD=plain
. /etc/sysconfig/authdaemon
if [ "$METHOD" = "mysql" ]; then
	if [ -f /var/lock/subsys/authdaemon ]; then
		/etc/rc.d/init.d/authdaemon restart >&2
	else
		echo "Run \"/etc/rc.d/init.d/authdaemon start\" to start courier-imap authdaemon."
	fi
fi

%preun authmysql
METHOD=plain
. /etc/sysconfig/authdaemon
if [ "$1" = "$0" -a "$METHOD" = "mysql" ]; then
	if [ -f /var/lock/subsys/authdaemon ]; then
		/etc/rc.d/init.d/authdaemon stop >&2
	fi
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/imap
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.imap
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/courier-imap
%attr(754,root,root) /etc/rc.d/init.d/courier-imap
%{_sysconfdir}/imapd.cnf
%attr(755,root,root) %{_bindir}/imapd
%attr(755,root,root) %{_sbindir}/imaplogin
%attr(755,root,root) %{_sbindir}/mkimapdcert
%{_mandir}/man8/imapd*

%files common
%defattr(644,root,root,755)
%doc README* imap/BUGS ChangeLog AUTHORS
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/authdaemon
%attr(754,root,root) /etc/rc.d/init.d/authdaemon
%attr(700,root,root) /var/lib/authdaemon
%attr(750,root,root) %dir %{_sysconfdir}
%dir %{_libexecdir}
%dir %{_libexecdir}/authlib
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/authdaemonrc
%{_sysconfdir}/quotawarnmsg.example
%attr(755,root,root) %{_bindir}/couriertls
%attr(755,root,root) %{_libexecdir}/authlib/authdaemon
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.plain
%attr(755,root,root) %{_libexecdir}/couriertcpd
%attr(755,root,root) %{_libexecdir}/courierlogger
%attr(755,root,root) %{_libexecdir}/makedatprog
%{_mandir}/man8/auth[cdsuv]*
%{_mandir}/man8/authp[aw]*
%{_mandir}/man7/authlib*
%{_mandir}/man1/couriert*
%{_mandir}/man8/mk*

%files userdb
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/makeuserdb
%attr(755,root,root) %{_sbindir}/pw2userdb
%attr(755,root,root) %{_sbindir}/userdb
%attr(755,root,root) %{_sbindir}/userdbpw
%attr(755,root,root) %{_sbindir}/vchkpw2userdb
%{_mandir}/man8/makeuserdb*
%{_mandir}/man8/userdb*
%{_mandir}/man8/*pw2userdb*

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
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/pop3
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.pop3
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/courier-pop3
%attr(754,root,root) /etc/rc.d/init.d/courier-pop3
%attr(755,root,root) %{_bindir}/pop3d
%attr(755,root,root) %{_sbindir}/mkpop3dcert
%attr(755,root,root) %{_sbindir}/pop3login
%{_sysconfdir}/pop3d.cnf
%{_mandir}/man8/courierpop*

%if %{?_without_ldap:0}%{!?_without_ldap:1}
%files authldap
%defattr(644,root,root,755)
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/authldaprc
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.ldap
%{_mandir}/man8/authldap*
%endif

%if %{?_without_mysql:0}%{!?_without_mysql:1}
%files authmysql
%defattr(644,root,root,755)
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/authmysqlrc
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.mysql
%{_mandir}/man8/authmysql*
%endif

%if %{?_without_pgsql:0}%{!?_without_pgsql:1}
%files authpgsql
%defattr(644,root,root,755)
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/authpgsqlrc
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.pgsql
%{_mandir}/man8/authpgsql*
%endif
