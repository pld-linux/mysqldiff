Summary:	Tool to detect layout differences between two MySQL databases
Summary(pl.UTF-8):	Narzędzie do wykrywania różnic układu pomiędzy dwoma bazami MySQL
Name:		mysqldiff
Version:	1.5.0
Release:	0.2
License:	freeware
Group:		Applications/WWW
# Source0Download:	http://www.mysqldiff.org/file.php?id=23
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	027d52697950030a550af903f5f6cb1e
URL:		http://www.mysqldiff.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	webapps
Requires:	webserver(php) >= 4.1.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
MySQLdiff is a little Tool to detect layout differences between two
databases.

MySQLdiff will create a SQL-ALTER-Script which has to be run onto the
live-system to 'patch' it to the state of the developement system.

%description -l pl.UTF-8
MySQLdiff jest narzędzie do wykrywania różnic układu pomiędzy dwoma
bazami MySQL.

MySQLdiff tworzy skrypt z poleceniami SQL ALTER, który należy wykonać
na systemie produkcyjnym aby zmodyfikować jego zawartość do stanu
systemu rozwojowego.

%prep
%setup -q

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

cp -a . $RPM_BUILD_ROOT%{_appdir}
rm -rf $RPM_BUILD_ROOT%{_appdir}/docs
rm -f $RPM_BUILD_ROOT%{_appdir}/apache.conf
mv $RPM_BUILD_ROOT%{_appdir}/config.inc.php.dist $RPM_BUILD_ROOT%{_sysconfdir}/config.php
ln -s %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_appdir}/config.inc.php

install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc docs/CHANGES
%doc %lang(de) docs/LIESMICH.txt
%doc %lang(nl) docs/LISEZMOI.txt
%doc docs/README.txt

%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/javascript
%{_appdir}/library
%{_appdir}/screens
%{_appdir}/style

%dir %{_appdir}/nls
%{_appdir}/nls/english-iso-8859-1.nls.php
%lang(de) %{_appdir}/nls/german-iso-8859-1.nls.php
%lang(fr) %{_appdir}/nls/french-iso-8859-1.nls.php
%lang(hu) %{_appdir}/nls/hungarian-iso-8859-2.nls.php
%lang(nl) %{_appdir}/nls/dutch-iso-8859-1.nls.php
%lang(nl) %{_appdir}/nls/dutch-iso-8859-1.nls.php
%lang(ru) %{_appdir}/nls/russian-cp1251.nls.php
%lang(ru) %{_appdir}/nls/russian-koi8-r.nls.php
