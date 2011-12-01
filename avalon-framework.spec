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
Release:     5
Summary:     Java components interfaces
License:     ASL 2.0
URL:         http://avalon.apache.org/%{short_name}/
Group:       Development/Java
Source0:     http://archive.apache.org/dist/excalibur/avalon-framework/source/%{name}-api-%{version}-src.tar.gz
Source1:     http://archive.apache.org/dist/excalibur/avalon-framework/source/%{name}-impl-%{version}-src.tar.gz

# pom files are not provided in tarballs so get them from external site
Source2:     http://repo1.maven.org/maven2/avalon-framework/%{name}-api/%{version}/%{name}-api-%{version}.pom
Source3:     http://repo1.maven.org/maven2/avalon-framework/%{name}-impl/%{version}/%{name}-impl-%{version}.pom

# remove jmock from dependencies because we don't have it
Patch0:     %{name}-impl-pom.patch

Requires:    apache-commons-logging
Requires:    avalon-logkit
Requires:    log4j
Requires:    xalan-j2
Requires:    xml-commons-apis

Requires(post):    jpackage-utils
Requires(postun):  jpackage-utils

BuildRequires:    ant
BuildRequires:	  ant-junit
BuildRequires:	  apache-commons-logging
BuildRequires:    avalon-logkit
BuildRequires:    jpackage-utils
# For converting jar into OSGi bundle
BuildRequires:    aqute-bndlib
BuildRequires:    junit
BuildRequires:	  log4j
BuildRequires:    xml-commons-apis


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
Group:        Development/Java
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
popd

%build
export CLASSPATH=%(build-classpath avalon-logkit junit commons-logging log4j)
export CLASSPATH="$CLASSPATH:../target/%{name}-api-%{version}.jar"
ant jar test javadoc
# Convert to OSGi bundle
java -jar %{_javadir}/aqute-bndlib.jar wrap target/%{name}-api-%{version}.jar

# build implementation now
pushd %{name}-impl-%{version}
# tests removed because we don't have jmock
rm -rf src/test/*
ant jar javadoc
# Convert to OSGi bundle
java -jar %{_javadir}/aqute-bndlib.jar wrap target/%{name}-impl-%{version}.jar
popd

%install
install -d -m 755 %{buildroot}%{_javadir}/
install -d -m 755 %{buildroot}/%{_mavenpomdir}

install -m 644 target/%{name}-api-%{version}.bar %{buildroot}%{_javadir}/%{name}-api.jar
mkdir -p %{buildroot}%{_javadocdir}/%{name}/%{name}-api

# pom file
install -pm 644 %{name}-api-%{version}.pom %{buildroot}/%{_mavenpomdir}/JPP-%{name}-api.pom
%add_to_maven_depmap %{name} %{name}-api %{version} JPP %{name}-api
%add_to_maven_depmap org.apache.avalon.framework %{name}-api %{version} JPP %{name}-api

# javadocs
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}/%{name}-api/


pushd %{name}-impl-%{version}
install -m 644 target/%{name}-impl-%{version}.bar %{buildroot}%{_javadir}/%{name}-impl.jar
ln -sf %{_javadir}/%{name}-impl.jar %{buildroot}%{_javadir}/%{name}.jar

# pom file
install -pm 644 %{name}-impl-%{version}.pom %{buildroot}/%{_mavenpomdir}/JPP-%{name}-impl.pom
%add_to_maven_depmap %{name} %{name}-impl %{version} JPP %{name}-impl
%add_to_maven_depmap org.apache.avalon.framework %{name}-impl %{version} JPP %{name}-impl
%add_to_maven_depmap %{name} %{name} %{version} JPP %{name}-impl

# javadocs
mkdir -p %{buildroot}%{_javadocdir}/%{name}/%{name}-impl
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}/%{name}-impl/
popd

%post
%update_maven_depmap

%postun
%update_maven_depmap


%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt
%{_mavenpomdir}/JPP-%{name}-api.pom
%{_mavenpomdir}/JPP-%{name}-impl.pom
%{_javadir}/%{name}-api.jar
%{_javadir}/%{name}-impl.jar
%{_javadir}/%{name}.jar
%{_mavendepmapfragdir}/%{name}

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}

