Summary:	Courier-IMAP 0.18 IMAP server
Name:		courier-imap
Version:	0.22
Release:	1
License:	GPL
Group:		Applications/Mail
Group(pl):	Aplikacje/Poczta
Group(pt):	Aplicações/Correio Eletrônico
Source0:	http://www.inter7.com/courierimap/%{name}-%{version}.tar.gz
Source1:	%{name}.initd
Source2:	%{name}.pamd
Source3:	%{name}.sysconfig
URL:		http://www.inter7.com/courierimap/
BuildRoot:	/tmp/%{name}-%{version}-root
Provides:	imapdaemon
Obsoletes:	imapdaemon

%define		_libexecdir	/usr/lib/courier-imap

%description
Courier-IMAP is an IMAP server for Maildir mailboxes.

%prep
%setup -q
%build
LDFLAGS="-s"; export LDFLAGS
%configure \
	--with-authvchkpw
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{pam.d,rc.d/init.d,security,sysconfig}

make install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/courier-imap
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/imap
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/courier-imap

mv imap/README README.imap
mv maildir/README.maildirquota.txt README.maildirquota

rm -rf $RPM_BUILD_ROOT%{_mandir}/man8/{authcram,authpam,authpwd,authshadow,authuserdb,authvchkpw,pw2userdb,vchkpw2userdb}.8

echo ".so authlib.8" >$RPM_BUILD_ROOT%{_mandir}/man8/authcram.8
echo ".so authlib.8" >$RPM_BUILD_ROOT%{_mandir}/man8/authpam.8
echo ".so authlib.8" >$RPM_BUILD_ROOT%{_mandir}/man8/authpwd.8
echo ".so authlib.8" >$RPM_BUILD_ROOT%{_mandir}/man8/authshadow.8
echo ".so authlib.8" >$RPM_BUILD_ROOT%{_mandir}/man8/authuserdb.8
echo ".so authlib.8" >$RPM_BUILD_ROOT%{_mandir}/man8/authvchkpw.8
echo ".so makeuserdb.8" >$RPM_BUILD_ROOT%{_mandir}/man8/pw2userdb.8
echo ".so makeuserdb.8" >$RPM_BUILD_ROOT%{_mandir}/man8/vchkpw2userdb.8

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/*/* README* imap/BUGS AUTHORS COPYING

touch $RPM_BUILD_ROOT/etc/security/blacklist.courier-imap

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {AUTHORS,COPYING,imap/BUGS,README,README.imap,README.maildirquota}.gz
%attr(640,root,root) %config /etc/pam.d/imap
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.courier-imap
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/courier-imap
%attr(754,root,root) /etc/rc.d/init.d/courier-imap
%dir %{_libexecdir}
%dir %{_libexecdir}/authlib
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libexecdir}/authlib/*
%attr(755,root,root) %{_libexecdir}/couriertcpd
%attr(755,root,root) %{_libexecdir}/deliverquota
%attr(755,root,root) %{_libexecdir}/logger
%attr(755,root,root) %{_libexecdir}/makedatprog
%{_mandir}/*/*
