%define short_name      framework
%define short_Name      Avalon
%define section         free
%define bootstrap       1
%define gcj_support     1

Name:           avalon-%{short_name}
Version:        4.3
Release:        3
Epoch:          0
Summary:        Java components interfaces
License:        Apache License
Url:            http://avalon.apache.org/%{short_name}/
Group:          Development/Java
#Vendor:        JPackage Project
#Distribution:  JPackage
Source0:        http://www.apache.org/dist/excalibur/excalibur-framework/source/avalon-framework-4.2.0-src.tar.bz2
Source1:        %{name}-build.xml
Requires:       log4j
BuildRequires:  ant
BuildRequires:  ant-junit
%if !%{bootstrap}
BuildRequires:  avalon-logkit
%endif
BuildRequires:  java-javadoc
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  junit
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRequires:  log4j
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The Avalon framework consists of interfaces that define relationships
between commonly used application components, best-of-practice pattern
enforcements, and several lightweight convenience implementations of the
generic components.
What that means is that we define the central interface Component. We
also define the relationship (contract) a component has with peers,
ancestors and children. This documentation introduces you to those
patterns, interfaces and relationships.

%package manual
Summary:        Manual for %{name}
Group:          Development/Java

%description manual
Documentation for %{name}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}
%{__cp} -a %{SOURCE1} build.xml
%{__perl} -pi -e 's/enum( |\.)/enum1\1/g' api/src/java/org/apache/avalon/framework/Enum.java

# fix end-of-line
%{__perl} -pi -e 's/\r$//g' LICENSE.txt NOTICE.TXT

for i in `find docs -type f`; do
    %{__perl} -pi -e 's/\r$//g' $i
done

%build
%if !%{bootstrap}
export CLASSPATH=$(build-classpath avalon-logkit junit log4j)
%else
export CLASSPATH=$(build-classpath junit log4j)
%endif
export OPT_JAR_LIST="`%{__cat} %{_sysconfdir}/ant.d/junit`"
%{ant} -Djava.javadoc=%{_javadocdir}/java jar doc test-all

%install
%{__rm} -rf %{buildroot}

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
install -m 644 dist/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
# create unversioned symlinks
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)
cp -pr doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

for i in `find $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version} -type f -name "*.html" -o -name "*.css"`; do
    %{__perl} -pi -e 's/\r$//g' $i
done

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt NOTICE.TXT
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files manual
%defattr(0644,root,root,0755)
%if 0
%doc docs/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}



%changelog
* Tue Mar 15 2011 Stéphane Téletchéa <steletch@mandriva.org> 0:4.3-1mdv2011.0
+ Revision: 645024
- update to new version 4.3

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 0:4.2.0-1.4.3mdv2011.0
+ Revision: 603485
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0:4.2.0-1.4.2mdv2010.1
+ Revision: 522113
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 0:4.2.0-1.4.1mdv2010.0
+ Revision: 413151
- rebuild

* Fri Jan 04 2008 David Walluck <walluck@mandriva.org> 0:4.2.0-1.4.0mdv2008.1
+ Revision: 145502
- fix build

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)
    - remove unnecessary Requires(post) on java-gcj-compat


* Wed Dec 13 2006 David Walluck <walluck@mandriva.org> 4.2.0-1.2mdv2007.0
+ Revision: 96200
- update Source URL
- update

* Tue Dec 12 2006 David Walluck <walluck@mandriva.org> 0:4.2.0-1.1mdv2007.1
+ Revision: 95176
- Import avalon-framework

* Tue Sep 05 2006 David Walluck <walluck@mandriva.org> 0:4.2.0-1.1mdv2007.0
- add missing (Build)Requires: log4j

* Fri Sep 01 2006 David Walluck <walluck@mandriva.org> 0:4.2.0-1mdv2007.0
- 4.2.0
- empty manual package
- use $ instead of %% for build-classpath
- set OPT_JAR_LIST for tests
- clean %%{buildroot} in %%install

* Mon Jun 12 2006 David Walluck <walluck@mandriva.org> 0:4.1.4-2.3mdv2007.0
- rebuild for libgcj.so.7
- aot compile
- fix build

* Sat May 14 2005 David Walluck <walluck@mandriva.org> 0:4.1.4-2.2mdk
- rebuild as non-bootstrap

* Fri May 13 2005 David Walluck <walluck@mandriva.org> 0:4.1.4-2.1mdk
- release

* Thu Nov 04 2004 Gary Benson <gbenson@redhat.com> 0:4.1.4-2jpp_5fc
- Build into Fedora.

* Fri Oct 29 2004 Gary Benson <gbenson@redhat.com> 0:4.1.4-2jpp_4fc
- Bootstrap into Fedora.

* Fri Oct 01 2004 Andrew Overholt <overholt@redhat.com> 0:4.1.4-2jpp_3rh
- Remove avalan-logkit as a Requires

* Mon Mar 08 2004 Frank Ch. Eigler <fche@redhat.com> 0:4.1.4-2jpp_2rh
- RH vacuuming part II

* Fri Mar 05 2004 Frank Ch. Eigler <fche@redhat.com> 0:4.1.4-2jpp_1rh
- RH vacuuming

