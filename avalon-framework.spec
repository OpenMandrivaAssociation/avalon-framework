%define short_name      framework
%define short_Name      Avalon
%define section         free
%define bootstrap       0
%define gcj_support     1

Name:           avalon-%{short_name}
Version:        4.2.0
Release:        %mkrel 1.4.2
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

