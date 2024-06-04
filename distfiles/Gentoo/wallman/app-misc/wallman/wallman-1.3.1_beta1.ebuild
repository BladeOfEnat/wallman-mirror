# Copyright 1999-2024 Gentoo Authors
# Distributed under the terms of the MIT License

EAPI=8

DISTUTILS_USE_PEP517=setuptools
PYTHON_COMPAT=( python3_{11,12} )
inherit distutils-r1 pypi

REAL_PV="${PV/_beta/b}"
DESCRIPTION="A python program that sets dynamic wallpapers on minimalistic Window Managers."
HOMEPAGE="https://git.entheuer.de/emma/wallman/"
SRC_URI="$(pypi_sdist_url "${PN^}" "${REAL_PV}")"

LICENSE="MIT"
SLOT="0"
KEYWORDS="~amd64 ~x86"

RDEPEND="
	dev-python/APScheduler[${PYTHON_USEDEP}]
	media-gfx/feh
	x11-libs/libnotify
"

BDEPEND="
	dev-python/setuptools[${PYTHON_USEDEP}]
"

python_prepare_all() {
	distutils-r1_python_prepare_all
}
python_compile() {
	distutils-r1_python_compile -j1
}
python_install() {
	distutils-r1_python_install
	# Add a symlink to make the scrupt callable from the commandline
    local scriptname="wallman.py"
    local target="/usr/bin/wallman"
	local scriptpath="$(python_get_sitedir)/${scriptname}"
	fperms +x "${scriptpath}"
    dosym "$(python_get_sitedir)/${scriptname}" "${target}"
}
