#
# TODO:
#	- triggers
#	- post, preun
#	- add maildir.patch (like in courier-mta)
#
# Conditional build:
%bcond_without ldap	# without LDAP support
%bcond_without mysql	# without MySQL support
%bcond_without pgsql	# without PostgreSQL support
Summary:	Courier-IMAP server
Summary(pl):	Serwer Courier-IMAP
Name:		courier-imap
Version:	3.0.5
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/courier/%{name}-%{version}.tar.bz2
# Source0-md5:	8b0c79997905dc46cfe4cc13be74ceaf
Source1:	%{name}.init
Source2:	%{name}-pop3.init
Source3:	%{name}.pamd
Source4:	%{name}-pop3.pamd
Patch0:		%{name}-dirs.patch
Patch1:		%{name}-certsdir.patch
URL:		http://www.inter7.com/courierimap/
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake
BuildRequires:	gdbm-devel
BuildRequires:	libstdc++-devel
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_ldap:BuildRequires:	openldap-devel}
BuildRequires:	openssl-devel >= 0.9.7d
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	procps
BuildRequires:	sysconftool
%{?with_mysql:BuildRequires:	zlib-devel}
PreReq:		%{name}-common = %{version}-%{release}
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	pam >= 0.77.3
Provides:	imapdaemon
Obsoletes:	imapdaemon
Conflicts:	cyrus-imapd
Conflicts:	imap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	/usr/%{_lib}/courier-imap
%define		_sysconfdir	/etc/courier-imap
%define         _certsdir       %{_sysconfdir}/certs

%description
Courier-IMAP is an IMAP server for Maildir mailboxes.

%description -l pl
Courier-IMAP jest serwerem IMAP dla skrzynek pocztowych Maildir.

%package common
Summary:	Common files for imap and pop3 daemons
Summary(pl):	Pliki wspólne dla serwerów imap i pop3
Group:		Networking/Daemons
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-deliverquota	= %{version}-%{release}
Requires:	%{name}-maildirmake	= %{version}-%{release}
Requires:	%{name}-userdb		= %{version}-%{release}
Requires:	procps

%description common
Common files for imap and pop3 daemons.

%description common -l pl
Pliki wspólne dla serwerów imap i pop3.

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
PreReq:		%{name}-common = %{version}-%{release}
Requires:	pam >= 0.77.3
Provides:	pop3daemon
Obsoletes:	pop3daemon
Conflicts:	cyrus-imapd
Conflicts:	imap-pop3
Conflicts:	solid-pop3d
Conflicts:	tpop3d

%description pop3
Courier-IMAP POP3 is an POP3 server for Maildir mailboxes.

%description pop3 -l pl
Courier-IMAP POP3 jest serwerem POP3 dla skrzynek pocztowych Maildir.

%package authldap
Summary:	LDAP authentication daemon for Courier IMAP
Summary(pl):	Demon autentykacji LDAP do Courier IMAP
Group:		Networking/Daemons
PreReq:		%{name}-common = %{version}-%{release}

%description authldap
This package provides LDAP authentication for Courier IMAP.

%description authldap -l pl
Ten pakiet pozwala na korzystanie z autentykacji LDAP w Courier IMAP.

%package authmysql
Summary:	MySQL authentication daemon for Courier IMAP
Summary(pl):	Demon autentykacji MySQL do Courier IMAP
Group:		Networking/Daemons
PreReq:		%{name}-common = %{version}-%{release}
Requires:	zlib

%description authmysql
This package provides MySQL authentication for Courier IMAP.

%description authmysql -l pl
Ten pakiet pozwala na korzystanie z autentykacji MySQL w Courier IMAP.

%package authpgsql
Summary:	PostgreSQL authentication daemon for Courier IMAP
Summary(pl):	Demon autentykacji PostgreSQL do Courier IMAP
Group:		Networking/Daemons
PreReq:		%{name}-common = %{version}-%{release}

%description authpgsql
This package provides PostgreSQL authentication for Courier IMAP.

%description authpgsql -l pl
Ten pakiet pozwala na korzystanie z autentykacji PostgreSQL w Courier
IMAP.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

install %{SOURCE1} courier-imap.in
install %{SOURCE2} courier-pop3.in

%build
cp -f /usr/share/automake/config.sub .
cp -f /usr/share/automake/config.sub maildir

%{__aclocal}
%{__automake}
%{__autoconf}

cd authlib
%{__aclocal}
%{__automake}
%{__autoconf}
cd ../imap
%{__aclocal}
%{__automake}
%{__autoconf}
cd ..

%configure \
	--libexecdir=%{_libexecdir} \
	--enable-unicode \
	--with-authchangepwdir=/var/tmp \
	--with-authdaemonvar=/var/lib/authdaemon \
	--with-certsdir=%{_certsdir} \
	%{?with_mysql:--with-mysql-libs=%{_libdir} --with-mysql-includes=%{_includedir}/mysql} \
	%{!?with_mysql:--without-authmysql} \
	%{?with_pgsql:--with-pgsql-libs=%{_libdir} --with-pgsql-includes=%{_includedir}/postgresql} \
	%{!?with_pgsql:--without-authpgsql} \
	%{!?with_ldap:--without-authldap}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{pam.d,rc.d/init.d,security,sysconfig} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/shared,%{_certsdir},/var/lib/authdaemon}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install courier-imap $RPM_BUILD_ROOT/etc/rc.d/init.d/courier-imap
install courier-pop3 $RPM_BUILD_ROOT/etc/rc.d/init.d/courier-pop3
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/imap
install %{SOURCE4} $RPM_BUILD_ROOT/etc/pam.d/pop3

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

echo ".so man7/authlib.7"	>$RPM_BUILD_ROOT%{_mandir}/man8/authcram.8
echo ".so man7/authlib.7"	>$RPM_BUILD_ROOT%{_mandir}/man8/authpam.8
echo ".so man7/authlib.7"	>$RPM_BUILD_ROOT%{_mandir}/man8/authpwd.8
echo ".so man7/authlib.7"	>$RPM_BUILD_ROOT%{_mandir}/man8/authshadow.8
echo ".so man7/authlib.7"	>$RPM_BUILD_ROOT%{_mandir}/man8/authuserdb.8
echo ".so man7/authlib.7"	>$RPM_BUILD_ROOT%{_mandir}/man8/authvchkpw.8
echo ".so man7/authlib.7"	>$RPM_BUILD_ROOT%{_mandir}/man8/authdaemon.8
echo ".so man7/authlib.7"	>$RPM_BUILD_ROOT%{_mandir}/man8/authdaemond.8
%{?with_pgsql:echo ".so man7/authlib.7"	>$RPM_BUILD_ROOT%{_mandir}/man8/authpgsql.8}
%{?with_mysql:echo ".so man7/authlib.7"	>$RPM_BUILD_ROOT%{_mandir}/man8/authmysql.8}
%{?with_ldap:echo ".so man7/authlib.7"	>$RPM_BUILD_ROOT%{_mandir}/man8/authldap.8}
echo ".so makeuserdb.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/pw2userdb.8
echo ".so makeuserdb.8"	>$RPM_BUILD_ROOT%{_mandir}/man8/vchkpw2userdb.8

touch $RPM_BUILD_ROOT/etc/security/blacklist.{pop3,imap}

# make config files
./sysconftool $RPM_BUILD_ROOT%{_sysconfdir}/*.dist

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/*.dist

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

%triggerpostin -- %{name} < 3.0.5
echo pop3d.pem has been moved automatically to %{_certsdir}
mv -f /var/lib/openssl/imapd.pem %{_certsdir}

%triggerin -n %{name}-common -- %{name}-common < 3.0.5
/sbin/chkconfig --del authdaemon
rm -f /var/lock/subsys/authdaemon

%post pop3
/sbin/chkconfig --add courier-pop3
/sbin/chkconfig --del courier-imap-pop3 >/dev/null 2>&1 || :
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
	/sbin/chkconfig --del courier-imap-pop3 >/dev/null 2>&1 || :
	rm -f /etc/rc.d/init.d/courier-imap-pop3
fi

%triggerpostin -n %{name}-pop3 -- %{name}-pop3 < 3.0.5
echo pop3d.pem has been moved automatically to %{_certsdir}
mv -f /var/lib/openssl/pop3d.pem %{_certsdir}

%post authldap
if ps -A |grep -q authdaemond.lda; then
        %{_libexecdir}/authlib/authdaemond stop
        %{_libexecdir}/authlib/authdaemond start
fi

%postun authldap
if [ -x %{_libexecdir}/authlib/authdaemond ]; then
        if ps -A |grep -q authdaemond.lda; then
                %{_libexecdir}/authlib/authdaemond stop;
                %{_libexecdir}/authlib/authdaemond start;
        fi
fi

%post authmysql
if ps -A |grep -q authdaemond.mys; then
        %{_libexecdir}/authlib/authdaemond stop
        %{_libexecdir}/authlib/authdaemond start
fi

%postun authmysql
if [ -x %{_libexecdir}/authlib/authdaemond ]; then
        if ps -A |grep -q authdaemond.mys; then
                %{_libexecdir}/authlib/authdaemond stop;
                %{_libexecdir}/authlib/authdaemond start;
        fi
fi

%post authpgsql
if ps -A |grep -q authdaemond.pgs; then
        %{_libexecdir}/authlib/authdaemond stop
        %{_libexecdir}/authlib/authdaemond start
fi

%postun authpgsql
if [ -x %{_libexecdir}/authlib/authdaemond ]; then
        if ps -A |grep -q authdaemond.pgs; then
                %{_libexecdir}/authlib/authdaemond stop;
                %{_libexecdir}/authlib/authdaemond start;
        fi
fi

%files
%defattr(644,root,root,755)
%doc maildir/README.sharedfolders.html
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/imap
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.imap
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/imapd
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/imapd-ssl
%{_sysconfdir}/imapd.cnf
%attr(754,root,root) /etc/rc.d/init.d/courier-imap
%attr(750,daemon,daemon) %dir %{_sysconfdir}/shared
%attr(755,root,root) %{_bindir}/imapd
%attr(755,root,root) %{_bindir}/maildiracl
%attr(755,root,root) %{_bindir}/maildirkw
%attr(755,root,root) %{_sbindir}/authenumerate
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
%attr(700,root,root) /var/lib/authdaemon
%attr(750,root,root) %dir %{_sysconfdir}
%attr(750,root,root) %dir %{_certsdir}
%dir %{_libexecdir}
%dir %{_libexecdir}/authlib
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/authdaemonrc
%{_sysconfdir}/quotawarnmsg.example
%attr(755,root,root) %{_bindir}/couriertls
%attr(755,root,root) %{_libexecdir}/authlib/authdaemon
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.plain
%attr(755,root,root) %{_libexecdir}/couriertcpd
%attr(755,root,root) %{_libexecdir}/makedatprog
%attr(755,root,root) %{_sbindir}/courierlogger
%{_mandir}/man8/auth[cdsuv]*
%{_mandir}/man8/authp[aw]*
%{_mandir}/man7/authlib*
%{_mandir}/man1/couriert*
%{_mandir}/man8/couriert*
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
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pop3d
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pop3d-ssl
%attr(754,root,root) /etc/rc.d/init.d/courier-pop3
%attr(755,root,root) %{_bindir}/pop3d
%attr(755,root,root) %{_sbindir}/mkpop3dcert
%attr(755,root,root) %{_sbindir}/pop3login
%attr(755,root,root) %{_libexecdir}/pop3d.rc
%attr(755,root,root) %{_libexecdir}/pop3d-ssl.rc
%{_sysconfdir}/pop3d.cnf
%{_mandir}/man8/courierpop*

%if %{with ldap}
%files authldap
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/authldaprc
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.ldap
%{_mandir}/man8/authldap*
%endif

%if %{with mysql}
%files authmysql
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/authmysqlrc
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.mysql
%{_mandir}/man8/authmysql*
%endif

%if %{with pgsql}
%files authpgsql
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/authpgsqlrc
%attr(755,root,root) %{_libexecdir}/authlib/authdaemond.pgsql
%{_mandir}/man8/authpgsql*
%endif
