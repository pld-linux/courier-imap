Summary:	Courier-IMAP 0.18 IMAP server
Name:		courier-imap
Version:	0.18
Release:	1
Copyright:	GPL
Group:		Applications/Mail
Source:		http://www.inter7.com/courierimap/%{name}-%{version}.tar.gz
URL:		http://www.inter7.com/courierimap/
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Courier-IMAP is an IMAP server for Maildir mailboxes.

%prep
%setup -q

#
# Always include authvchkpw, even if the build machine does not have it.
#

./configure --with-authvchkpw --prefix=/usr/lib/courier-imap\
%build
make
make check
%install

rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/pam.d
make install-strip DESTDIR=$RPM_BUILD_ROOT

#
# Red Hat init.d file
#

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

cat >$RPM_BUILD_ROOT/etc/rc.d/init.d/courier-imap <<EOF
#!/bin/sh
#
# chkconfig: 2345 80 30
# description: Courier-IMAP - IMAP server
#
#
#

case "\$1" in
start)
        cd /
	. /usr/lib/courier-imap/lib/imapd.config
	case x\$IMAPDSTART in
	x[yY]*)
		# Start daemons.
		touch /var/lock/subsys/courier-imap

		echo -n "Starting Courier-IMAP server:"
		/usr/lib/courier-imap/lib/imapd.rc start
		echo " imaplogin"
		;;
	esac
	;;
stop)
        echo -n "Stopping Courier-IMAP server:"
	/usr/lib/courier-imap/lib/imapd.rc stop
	echo " imaplogin"
	;;
restart)
	\$0 stop
	\$0 start
        ;;
esac
exit 0
EOF

#
# Fix imapd.config
#

sed 's/^IMAPDSTART=.*/IMAPDSTART=YES/' \
	<$RPM_BUILD_ROOT/usr/lib/courier-imap/lib/imapd.config \
	>$RPM_BUILD_ROOT/usr/lib/courier-imap/lib/imapd.config.tmp

mv $RPM_BUILD_ROOT/usr/lib/courier-imap/lib/imapd.config.tmp \
	$RPM_BUILD_ROOT/usr/lib/courier-imap/lib/imapd.config


#
# Red Hat /etc/profile.d scripts
#

mkdir -p $RPM_BUILD_ROOT/etc/profile.d
cat >$RPM_BUILD_ROOT/etc/profile.d/courier-imap.sh <<EOF
if echo "\$MANPATH" | tr ':' '\012' | fgrep -qx /usr/lib/courier-imap/man
then
:
else
	MANPATH="/usr/lib/courier-imap/man:\$MANPATH"
	export MANPATH
fi
EOF

cat >$RPM_BUILD_ROOT/etc/profile.d/courier-imap.csh <<EOF

echo "\$MANPATH" | tr ':' '\012' | fgrep -qx /usr/lib/courier-imap/man

if ( \$? ) then
	true
else
	if ( \$?MANPATH ) then
	  true
	else
	  setenv MANPATH ""
	endif
	setenv MANPATH "/usr/lib/courier-imap/man:\$MANPATH"
endif
EOF

#
# Compress everything in man
#

find $RPM_BUILD_ROOT/usr/lib/courier-imap/man ! -type d -print | perl -e '

	while (<>)
	{
		chop if /\n$/;
		$file=$_;
		if ( -l $file)
		{
                        symlink readlink("$file")
                                . ".gz", "$file.gz";
			unlink($file);
                }
                else
                {
                        system("gzip <$file >$file.gz");
			unlink($file);
		}
	}
'

for f in `cat authlib/modulelist`
do
	echo "/usr/lib/courier-imap/lib/$f"
done >filelist

cp imap/README README.imap
cp maildir/README.maildirquota.txt README.maildirquota

%post
/sbin/chkconfig --add courier-imap

%preun

if test "$1" = "0"
then
	/sbin/chkconfig --del courier-imap
fi

/usr/lib/courier-imap/lib/imapd.rc stop

%files -f filelist
%defattr(644,root,root,755)
%config /etc/pam.d/imap
%config /etc/profile.d/courier-imap.csh
%config /etc/profile.d/courier-imap.sh
%attr(755, bin, bin) /etc/rc.d/init.d/courier-imap
%dir /usr/lib/courier-imap
%dir /usr/lib/courier-imap/lib
/usr/lib/courier-imap/lib/couriertcpd
%config /usr/lib/courier-imap/lib/imapd.config
/usr/lib/courier-imap/lib/imapd.rc
/usr/lib/courier-imap/lib/makedatprog
/usr/lib/courier-imap/lib/deliverquota
/usr/lib/courier-imap/lib/logger
/usr/lib/courier-imap/bin
/usr/lib/courier-imap/man
%doc AUTHORS COPYING imap/BUGS README README.imap README.maildirquota
