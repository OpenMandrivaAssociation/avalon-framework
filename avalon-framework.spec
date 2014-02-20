%{?_javapackages_macros:%_javapackages_macros}
# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global short_name    framework
%global short_Name    Avalon

Name:        avalon-%{short_name}
Version:     4.3
Release:     9.1%{?dist}
Epoch:       0
Summary:     Java components interfaces
License:     ASL 2.0
URL:         http://avalon.apache.org/%{short_name}/

Source0:     http://archive.apache.org/dist/excalibur/avalon-framework/source/%{name}-api-%{version}-src.tar.gz
Source1:     http://archive.apache.org/dist/excalibur/avalon-framework/source/%{name}-impl-%{version}-src.tar.gz

# pom files are not provided in tarballs so get them from external site
Source2:     http://repo1.maven.org/maven2/avalon-framework/%{name}-api/%{version}/%{name}-api-%{version}.pom
Source3:     http://repo1.maven.org/maven2/avalon-framework/%{name}-impl/%{version}/%{name}-impl-%{version}.pom

# remove jmock from dependencies because we don't have it
Patch0:     %{name}-impl-pom.patch
Patch1:     %{name}-xerces.patch

Requires:    apache-commons-logging
Requires:    avalon-logkit
Requires:    log4j
Requires:    xalan-j2

BuildRequires:    ant
BuildRequires:	  ant-junit
BuildRequires:	  apache-commons-logging
BuildRequires:    avalon-logkit
BuildRequires:    jpackage-utils
# For converting jar into OSGi bundle
BuildRequires:    aqute-bnd
BuildRequires:    junit
BuildRequires:	  log4j


BuildArch:    	  noarch

Obsoletes:    %{name}-manual <= 0:4.1.4

%description
The Avalon framework consists of interfaces that define relationships
between commonly used application components, best-of-practice pattern
enforcements, and several lightweight convenience implementations of the
generic components.
What that means is that we define the central interface Component. We
also define the relationship (contract) a component has with peers,
ancestors and children.

%package javadoc
Summary:      API documentation %{name}

Requires:     jpackage-utils

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}-api-%{version}
tar xvf %{SOURCE1}

cp %{SOURCE2} .

pushd %{name}-impl-%{version}/
cp %{SOURCE3} .
%patch0
%patch1 -p2
popd

%build
export CLASSPATH=%(build-classpath avalon-logkit junit commons-logging log4j)
export CLASSPATH="$CLASSPATH:../target/%{name}-api-%{version}.jar"
ant jar test javadoc
# Convert to OSGi bundle
java -jar $(build-classpath aqute-bnd) wrap target/%{name}-api-%{version}.jar

# build implementation now
pushd %{name}-impl-%{version}
# tests removed because we don't have jmock
rm -rf src/test/*
ant jar javadoc
# Convert to OSGi bundle
java -jar $(build-classpath aqute-bnd) wrap target/%{name}-impl-%{version}.jar
popd

%install
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/
install -d -m 755 $RPM_BUILD_ROOT/%{_mavenpomdir}

install -m 644 target/%{name}-api-%{version}.bar $RPM_BUILD_ROOT%{_javadir}/%{name}-api.jar
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}/%{name}-api

# pom file
install -pm 644 %{name}-api-%{version}.pom $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{name}-api.pom
%add_maven_depmap JPP-%{name}-api.pom %{name}-api.jar -a "org.apache.avalon.framework:%{name}-api"

# javadocs
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}/%{name}-api/


pushd %{name}-impl-%{version}
install -m 644 target/%{name}-impl-%{version}.bar $RPM_BUILD_ROOT%{_javadir}/%{name}-impl.jar
ln -sf %{_javadir}/%{name}-impl.jar ${RPM_BUILD_ROOT}%{_javadir}/%{name}.jar

# pom file
install -pm 644 %{name}-impl-%{version}.pom $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{name}-impl.pom
%add_maven_depmap JPP-%{name}-impl.pom %{name}-impl.jar -a "org.apache.avalon.framework:%{name}-impl,%{name}:%{name}"

# javadocs
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}/%{name}-impl
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}/%{name}-impl/
popd


%files
%doc LICENSE.txt NOTICE.txt
%{_mavenpomdir}/JPP-%{name}-api.pom
%{_mavenpomdir}/JPP-%{name}-impl.pom
%{_javadir}/%{name}-api.jar
%{_javadir}/%{name}-impl.jar
%{_javadir}/%{name}.jar
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Tomas Radej <tradej@redhat.com> - 0:4.3-6
- Fixed xerces dep

* Fri Apr 6 2012 Alexander Kurtakov <akurtako@redhat.com> 0:4.3-5
- Remove unneeded BR/R.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:4.3-3
- aqute-bndlib renamed to aqute-bnd (#745163)
- Use new maven macros
- Packaging tweaks

* Tue May 3 2011 Severin Gehwolf <sgehwolf@redhat.com> 0:4.3-3
- Convert jar's to OSGi bundles using aqute-bndlib.

* Tue May  3 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:4.3-2
- Add compatibility depmap for org.apache.avalon.framework groupId

* Wed Apr 20 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:4.3-1
- Latest version
- Split into two jars, provide backward compatible symlink
- Cleanups according to new guidelines

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 Alexander Kurtakov <akurtako@redhat.com> 0:4.1.4-7
- Drop gcj.
- Use global.
- No versioned jars.
- Fix permissions.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:4.1.4-4
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:4.1.4-3jpp.14
- Autorebuild for GCC 4.3

* Thu Mar 08 2007 Permaine Cheung <pcheung at redhat.com> - 0:4.1.4-2jpp.14
- rpmlint cleanup.

* Thu Aug 10 2006 Matt Wringe <mwringe at redhat.com> - 0:4.1.4-2jpp.13
- Add missing javadoc requires

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:4.1.4-2jpp_12fc
- Rebuilt

* Wed Jul 19 2006 Matt Wringe <mwringe at redhat.com> - 0:4.1.4-2jpp_11fc
- Removed separate definition of name, version and release.

* Wed Jul 19 2006 Matt Wringe <mwringe at redhat.com> - 0:4.1.4-2jpp_10fc
- Added conditional native compling.

* Thu Jun  8 2006 Deepak Bhole <dbhole@redhat.com> - 0:4.1.4-2jpp_9fc
- Updated description for fix to Bug# 170999

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:4.1.4-2jpp_8fc
- stop scriptlet spew

* Wed Dec 21 2005 Gary Benson <gbenson@redhat.com> 0:4.1.4-2jpp_7fc
- Rebuild again

* Thu Dec 15 2005 Gary Benson <gbenson@redhat.com> 0:4.1.4-2jpp_6fc
- Rebuild for new gcj.

* Thu Nov  4 2004 Gary Benson <gbenson@redhat.com> 0:4.1.4-2jpp_5fc
- Build into Fedora.

* Thu Oct 28 2004 Gary Benson <gbenson@redhat.com> 0:4.1.4-2jpp_4fc
- Bootstrap into Fedora.

* Thu Sep 30 2004 Andrew Overholt <overholt@redhat.com> 0:4.1.4-2jpp_3rh
- Remove avalon-logkit as a Requires

* Mon Mar  8 2004 Frank Ch. Eigler <fche@redhat.com> 0:4.1.4-2jpp_2rh
- RH vacuuming part II

* Fri Mar  5 2004 Frank Ch. Eigler <fche@redhat.com> 0:4.1.4-2jpp_1rh
- RH vacuuming

* Fri May 09 2003 David Walluck <david@anti-microsoft.org> 0:4.1.4-2jpp
- update for JPackage 1.5

* Fri Mar 21 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 4.1.4-1jpp
- For jpackage-utils 1.5
- Forrest is not used right now

* Tue May 07 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.1.2-3jpp
- hardcoded distribution and vendor tag
- group tag again

* Thu May 2 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.1.2-2jpp
- distribution tag
- group tag

* Sun Feb 03 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.1.2-1jpp
- 4.1.2
- section macro

* Thu Jan 17 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.1-2jpp
- versioned dir for javadoc
- no dependencies for manual and javadoc packages
- requires xml-commons-apis

* Wed Dec 12 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.1-1jpp
- 4.1
- Requires and BuildRequires xalan-j2

* Wed Dec 5 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.0-4jpp
- javadoc into javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 4.0-3jpp
- changed extension --> jpp

* Sat Oct 6 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.0-2jpp
- first unified release
- used original tarball

* Thu Sep 13 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.0-1mdk
- first Mandrake release
