TEMPLATE = app
CONFIG += console c++2b
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += \
    ap_application.cpp \
    ap_session.cpp \
    ap_user.cpp \
    dbase.cpp \
    embeddableapp.cpp \
    imageprocessor.cpp \
    main.cpp \
    sh_application.cpp \
    sh_business.cpp \
    sh_persistdata.cpp \
    tools.cpp

DISTFILES += \
    .clangd \
    CMakeLists.txt \
    Dockerfile \
    embed.html \
    resources/ajax-loading.gif \
    resources/collapse-rtl.gif \
    resources/collapse.gif \
    resources/date.gif \
    resources/expand-rtl.gif \
    resources/expand.gif \
    resources/font-awesome/LICENSE.txt \
    resources/font-awesome/css/font-awesome.css \
    resources/font-awesome/css/font-awesome.min.css \
    resources/font-awesome/fonts/FontAwesome.otf \
    resources/font-awesome/fonts/fontawesome-webfont.eot \
    resources/font-awesome/fonts/fontawesome-webfont.svg \
    resources/font-awesome/fonts/fontawesome-webfont.ttf \
    resources/font-awesome/fonts/fontawesome-webfont.woff \
    resources/font-awesome/fonts/fontawesome-webfont.woff2 \
    resources/form.css \
    resources/html4_default.css \
    resources/icon_clock.gif \
    resources/images/logo.svg \
    resources/items-not-ok.gif \
    resources/items-ok.gif \
    resources/items.gif \
    resources/jPlayer/jquery.jplayer.js \
    resources/jPlayer/jquery.jplayer.min.js \
    resources/jPlayer/jquery.jplayer.swf \
    resources/jPlayer/jquery.min.js \
    resources/jPlayer/skin/jplayer.blue.monday.css \
    resources/jPlayer/skin/jplayer.blue.monday.jpg \
    resources/jPlayer/skin/jplayer.blue.monday.seeking.gif \
    resources/jPlayer/skin/jplayer.blue.monday.video.play.png \
    resources/line-last-rtl.gif \
    resources/line-last.gif \
    resources/line-middle-rtl.gif \
    resources/line-middle.gif \
    resources/line-trunk.gif \
    resources/loading.png \
    resources/minus.gif \
    resources/moz-transitions.css \
    resources/plus.gif \
    resources/resizable.png \
    resources/right-arrow.gif \
    resources/tab_b.gif \
    resources/tab_l.gif \
    resources/tab_r.gif \
    resources/themes/bootstrap/2/bootstrap-responsive.css \
    resources/themes/bootstrap/2/bootstrap-responsive.min.css \
    resources/themes/bootstrap/2/bootstrap.css \
    resources/themes/bootstrap/2/bootstrap.min.css \
    resources/themes/bootstrap/2/date-edit-button.png \
    resources/themes/bootstrap/2/date-edit-button.svg \
    resources/themes/bootstrap/2/nav-minus-rtl.gif \
    resources/themes/bootstrap/2/nav-minus.gif \
    resources/themes/bootstrap/2/nav-plus-rtl.gif \
    resources/themes/bootstrap/2/nav-plus.gif \
    resources/themes/bootstrap/2/spin-buttons.png \
    resources/themes/bootstrap/2/spin-buttons.svg \
    resources/themes/bootstrap/2/stripes/generate.sh \
    resources/themes/bootstrap/2/stripes/stripe-10px.gif \
    resources/themes/bootstrap/2/stripes/stripe-11px.gif \
    resources/themes/bootstrap/2/stripes/stripe-12px.gif \
    resources/themes/bootstrap/2/stripes/stripe-13px.gif \
    resources/themes/bootstrap/2/stripes/stripe-14px.gif \
    resources/themes/bootstrap/2/stripes/stripe-15px.gif \
    resources/themes/bootstrap/2/stripes/stripe-16px.gif \
    resources/themes/bootstrap/2/stripes/stripe-17px.gif \
    resources/themes/bootstrap/2/stripes/stripe-18px.gif \
    resources/themes/bootstrap/2/stripes/stripe-19px.gif \
    resources/themes/bootstrap/2/stripes/stripe-20px.gif \
    resources/themes/bootstrap/2/stripes/stripe-21px.gif \
    resources/themes/bootstrap/2/stripes/stripe-22px.gif \
    resources/themes/bootstrap/2/stripes/stripe-23px.gif \
    resources/themes/bootstrap/2/stripes/stripe-24px.gif \
    resources/themes/bootstrap/2/stripes/stripe-25px.gif \
    resources/themes/bootstrap/2/stripes/stripe-26px.gif \
    resources/themes/bootstrap/2/stripes/stripe-27px.gif \
    resources/themes/bootstrap/2/stripes/stripe-28px.gif \
    resources/themes/bootstrap/2/stripes/stripe-29px.gif \
    resources/themes/bootstrap/2/stripes/stripe-30px.gif \
    resources/themes/bootstrap/2/stripes/stripe-31px.gif \
    resources/themes/bootstrap/2/stripes/stripe-32px.gif \
    resources/themes/bootstrap/2/stripes/stripe-33px.gif \
    resources/themes/bootstrap/2/stripes/stripe-34px.gif \
    resources/themes/bootstrap/2/stripes/stripe-35px.gif \
    resources/themes/bootstrap/2/stripes/stripe-36px.gif \
    resources/themes/bootstrap/2/stripes/stripe-37px.gif \
    resources/themes/bootstrap/2/stripes/stripe-38px.gif \
    resources/themes/bootstrap/2/stripes/stripe-39px.gif \
    resources/themes/bootstrap/2/stripes/stripe-40px.gif \
    resources/themes/bootstrap/2/suggest-dropdown.png \
    resources/themes/bootstrap/2/suggest-dropdown.svg \
    resources/themes/bootstrap/2/time-edit-button.png \
    resources/themes/bootstrap/2/wt.css \
    resources/themes/bootstrap/2/wt.less \
    resources/themes/bootstrap/3/bootstrap-theme.css \
    resources/themes/bootstrap/3/bootstrap-theme.css.map \
    resources/themes/bootstrap/3/bootstrap-theme.min.css \
    resources/themes/bootstrap/3/bootstrap-theme.min.css.map \
    resources/themes/bootstrap/3/bootstrap.css \
    resources/themes/bootstrap/3/bootstrap.css.map \
    resources/themes/bootstrap/3/bootstrap.min.css \
    resources/themes/bootstrap/3/bootstrap.min.css.map \
    resources/themes/bootstrap/3/date-edit-button.png \
    resources/themes/bootstrap/3/date-edit-button.svg \
    resources/themes/bootstrap/3/nav-minus-rtl.gif \
    resources/themes/bootstrap/3/nav-minus.gif \
    resources/themes/bootstrap/3/nav-plus-rtl.gif \
    resources/themes/bootstrap/3/nav-plus.gif \
    resources/themes/bootstrap/3/spin-buttons.png \
    resources/themes/bootstrap/3/spin-buttons.svg \
    resources/themes/bootstrap/3/stripes/generate.sh \
    resources/themes/bootstrap/3/stripes/stripe-10px.gif \
    resources/themes/bootstrap/3/stripes/stripe-11px.gif \
    resources/themes/bootstrap/3/stripes/stripe-12px.gif \
    resources/themes/bootstrap/3/stripes/stripe-13px.gif \
    resources/themes/bootstrap/3/stripes/stripe-14px.gif \
    resources/themes/bootstrap/3/stripes/stripe-15px.gif \
    resources/themes/bootstrap/3/stripes/stripe-16px.gif \
    resources/themes/bootstrap/3/stripes/stripe-17px.gif \
    resources/themes/bootstrap/3/stripes/stripe-18px.gif \
    resources/themes/bootstrap/3/stripes/stripe-19px.gif \
    resources/themes/bootstrap/3/stripes/stripe-20px.gif \
    resources/themes/bootstrap/3/stripes/stripe-21px.gif \
    resources/themes/bootstrap/3/stripes/stripe-22px.gif \
    resources/themes/bootstrap/3/stripes/stripe-23px.gif \
    resources/themes/bootstrap/3/stripes/stripe-24px.gif \
    resources/themes/bootstrap/3/stripes/stripe-25px.gif \
    resources/themes/bootstrap/3/stripes/stripe-26px.gif \
    resources/themes/bootstrap/3/stripes/stripe-27px.gif \
    resources/themes/bootstrap/3/stripes/stripe-28px.gif \
    resources/themes/bootstrap/3/stripes/stripe-29px.gif \
    resources/themes/bootstrap/3/stripes/stripe-30px.gif \
    resources/themes/bootstrap/3/stripes/stripe-31px.gif \
    resources/themes/bootstrap/3/stripes/stripe-32px.gif \
    resources/themes/bootstrap/3/stripes/stripe-33px.gif \
    resources/themes/bootstrap/3/stripes/stripe-34px.gif \
    resources/themes/bootstrap/3/stripes/stripe-35px.gif \
    resources/themes/bootstrap/3/stripes/stripe-36px.gif \
    resources/themes/bootstrap/3/stripes/stripe-37px.gif \
    resources/themes/bootstrap/3/stripes/stripe-38px.gif \
    resources/themes/bootstrap/3/stripes/stripe-39px.gif \
    resources/themes/bootstrap/3/stripes/stripe-40px.gif \
    resources/themes/bootstrap/3/suggest-dropdown.png \
    resources/themes/bootstrap/3/suggest-dropdown.svg \
    resources/themes/bootstrap/3/time-edit-button.png \
    resources/themes/bootstrap/3/wt.css \
    resources/themes/bootstrap/3/wt.less \
    resources/themes/bootstrap/5/bootstrap.bundle.min.js \
    resources/themes/bootstrap/5/bootstrap.bundle.min.js.map \
    resources/themes/bootstrap/5/calendar-date.svg \
    resources/themes/bootstrap/5/main.css \
    resources/themes/bootstrap/5/main.css.map \
    resources/themes/bootstrap/5/nav-minus-rtl.gif \
    resources/themes/bootstrap/5/nav-minus.gif \
    resources/themes/bootstrap/5/nav-plus-rtl.gif \
    resources/themes/bootstrap/5/nav-plus.gif \
    resources/themes/bootstrap/img/glyphicons-halflings-white.png \
    resources/themes/bootstrap/img/glyphicons-halflings.png \
    resources/themes/bootstrap/sort-arrow-down.gif \
    resources/themes/bootstrap/sort-arrow-none.gif \
    resources/themes/bootstrap/sort-arrow-up.gif \
    resources/themes/bootstrap/splitter-h.png \
    resources/themes/bootstrap/splitter-v.png \
    resources/themes/default/closeicons-dialog.png \
    resources/themes/default/closeicons-mi.png \
    resources/themes/default/closeicons-tab.png \
    resources/themes/default/dropdown.png \
    resources/themes/default/nav-minus-rtl.gif \
    resources/themes/default/nav-minus.gif \
    resources/themes/default/nav-plus-rtl.gif \
    resources/themes/default/nav-plus.gif \
    resources/themes/default/no-stripes/generate.sh \
    resources/themes/default/no-stripes/no-stripe-10px.gif \
    resources/themes/default/no-stripes/no-stripe-11px.gif \
    resources/themes/default/no-stripes/no-stripe-12px.gif \
    resources/themes/default/no-stripes/no-stripe-13px.gif \
    resources/themes/default/no-stripes/no-stripe-14px.gif \
    resources/themes/default/no-stripes/no-stripe-15px.gif \
    resources/themes/default/no-stripes/no-stripe-16px.gif \
    resources/themes/default/no-stripes/no-stripe-17px.gif \
    resources/themes/default/no-stripes/no-stripe-18px.gif \
    resources/themes/default/no-stripes/no-stripe-19px.gif \
    resources/themes/default/no-stripes/no-stripe-20px.gif \
    resources/themes/default/no-stripes/no-stripe-21px.gif \
    resources/themes/default/no-stripes/no-stripe-22px.gif \
    resources/themes/default/no-stripes/no-stripe-23px.gif \
    resources/themes/default/no-stripes/no-stripe-24px.gif \
    resources/themes/default/no-stripes/no-stripe-25px.gif \
    resources/themes/default/no-stripes/no-stripe-26px.gif \
    resources/themes/default/no-stripes/no-stripe-27px.gif \
    resources/themes/default/no-stripes/no-stripe-28px.gif \
    resources/themes/default/no-stripes/no-stripe-29px.gif \
    resources/themes/default/no-stripes/no-stripe-30px.gif \
    resources/themes/default/no-stripes/no-stripe-31px.gif \
    resources/themes/default/no-stripes/no-stripe-32px.gif \
    resources/themes/default/no-stripes/no-stripe-33px.gif \
    resources/themes/default/no-stripes/no-stripe-34px.gif \
    resources/themes/default/no-stripes/no-stripe-35px.gif \
    resources/themes/default/no-stripes/no-stripe-36px.gif \
    resources/themes/default/no-stripes/no-stripe-37px.gif \
    resources/themes/default/no-stripes/no-stripe-38px.gif \
    resources/themes/default/no-stripes/no-stripe-39px.gif \
    resources/themes/default/no-stripes/no-stripe-40px.gif \
    resources/themes/default/slider-thumb-h-disabled.gif \
    resources/themes/default/slider-thumb-h.gif \
    resources/themes/default/slider-thumb-v-disabled.gif \
    resources/themes/default/slider-thumb-v.gif \
    resources/themes/default/sliderbg-h-disabled.png \
    resources/themes/default/sliderbg-h.png \
    resources/themes/default/sliderbg-v-disabled.png \
    resources/themes/default/sliderbg-v.png \
    resources/themes/default/sort-arrow-disabled.gif \
    resources/themes/default/sort-arrow-down.gif \
    resources/themes/default/sort-arrow-none.gif \
    resources/themes/default/sort-arrow-up.gif \
    resources/themes/default/spin-buttons-dn.png \
    resources/themes/default/spin-buttons-up.png \
    resources/themes/default/spin-buttons.png \
    resources/themes/default/splitter-h.png \
    resources/themes/default/splitter-v.png \
    resources/themes/default/stripes/generate.sh \
    resources/themes/default/stripes/stripe-10px.gif \
    resources/themes/default/stripes/stripe-11px.gif \
    resources/themes/default/stripes/stripe-12px.gif \
    resources/themes/default/stripes/stripe-13px.gif \
    resources/themes/default/stripes/stripe-14px.gif \
    resources/themes/default/stripes/stripe-15px.gif \
    resources/themes/default/stripes/stripe-16px.gif \
    resources/themes/default/stripes/stripe-17px.gif \
    resources/themes/default/stripes/stripe-18px.gif \
    resources/themes/default/stripes/stripe-19px.gif \
    resources/themes/default/stripes/stripe-20px.gif \
    resources/themes/default/stripes/stripe-21px.gif \
    resources/themes/default/stripes/stripe-22px.gif \
    resources/themes/default/stripes/stripe-23px.gif \
    resources/themes/default/stripes/stripe-24px.gif \
    resources/themes/default/stripes/stripe-25px.gif \
    resources/themes/default/stripes/stripe-26px.gif \
    resources/themes/default/stripes/stripe-27px.gif \
    resources/themes/default/stripes/stripe-28px.gif \
    resources/themes/default/stripes/stripe-29px.gif \
    resources/themes/default/stripes/stripe-30px.gif \
    resources/themes/default/stripes/stripe-31px.gif \
    resources/themes/default/stripes/stripe-32px.gif \
    resources/themes/default/stripes/stripe-33px.gif \
    resources/themes/default/stripes/stripe-34px.gif \
    resources/themes/default/stripes/stripe-35px.gif \
    resources/themes/default/stripes/stripe-36px.gif \
    resources/themes/default/stripes/stripe-37px.gif \
    resources/themes/default/stripes/stripe-38px.gif \
    resources/themes/default/stripes/stripe-39px.gif \
    resources/themes/default/stripes/stripe-40px.gif \
    resources/themes/default/wt.css \
    resources/themes/default/wt_ie.css \
    resources/themes/default/wt_ie6.css \
    resources/themes/polished/closeicons-dialog.png \
    resources/themes/polished/closeicons-mi.png \
    resources/themes/polished/closeicons-tab.png \
    resources/themes/polished/dropdown.png \
    resources/themes/polished/dropshadow.png \
    resources/themes/polished/gradient.png \
    resources/themes/polished/nav-minus-rtl.gif \
    resources/themes/polished/nav-minus-rtl.png \
    resources/themes/polished/nav-minus.gif \
    resources/themes/polished/nav-minus.png \
    resources/themes/polished/nav-plus-rtl.gif \
    resources/themes/polished/nav-plus-rtl.png \
    resources/themes/polished/nav-plus.gif \
    resources/themes/polished/nav-plus.png \
    resources/themes/polished/no-stripes/generate.sh \
    resources/themes/polished/no-stripes/no-stripe-10px.gif \
    resources/themes/polished/no-stripes/no-stripe-11px.gif \
    resources/themes/polished/no-stripes/no-stripe-12px.gif \
    resources/themes/polished/no-stripes/no-stripe-13px.gif \
    resources/themes/polished/no-stripes/no-stripe-14px.gif \
    resources/themes/polished/no-stripes/no-stripe-15px.gif \
    resources/themes/polished/no-stripes/no-stripe-16px.gif \
    resources/themes/polished/no-stripes/no-stripe-17px.gif \
    resources/themes/polished/no-stripes/no-stripe-18px.gif \
    resources/themes/polished/no-stripes/no-stripe-19px.gif \
    resources/themes/polished/no-stripes/no-stripe-20px.gif \
    resources/themes/polished/no-stripes/no-stripe-21px.gif \
    resources/themes/polished/no-stripes/no-stripe-22px.gif \
    resources/themes/polished/no-stripes/no-stripe-23px.gif \
    resources/themes/polished/no-stripes/no-stripe-24px.gif \
    resources/themes/polished/no-stripes/no-stripe-25px.gif \
    resources/themes/polished/no-stripes/no-stripe-26px.gif \
    resources/themes/polished/no-stripes/no-stripe-27px.gif \
    resources/themes/polished/no-stripes/no-stripe-28px.gif \
    resources/themes/polished/no-stripes/no-stripe-29px.gif \
    resources/themes/polished/no-stripes/no-stripe-30px.gif \
    resources/themes/polished/no-stripes/no-stripe-31px.gif \
    resources/themes/polished/no-stripes/no-stripe-32px.gif \
    resources/themes/polished/no-stripes/no-stripe-33px.gif \
    resources/themes/polished/no-stripes/no-stripe-34px.gif \
    resources/themes/polished/no-stripes/no-stripe-35px.gif \
    resources/themes/polished/no-stripes/no-stripe-36px.gif \
    resources/themes/polished/no-stripes/no-stripe-37px.gif \
    resources/themes/polished/no-stripes/no-stripe-38px.gif \
    resources/themes/polished/no-stripes/no-stripe-39px.gif \
    resources/themes/polished/no-stripes/no-stripe-40px.gif \
    resources/themes/polished/slider-thumb-disabled.png \
    resources/themes/polished/slider-thumb.png \
    resources/themes/polished/sliderbg-h-disabled.png \
    resources/themes/polished/sliderbg-h.png \
    resources/themes/polished/sliderbg-he-disabled.png \
    resources/themes/polished/sliderbg-he.png \
    resources/themes/polished/sliderbg-hw-disabled.png \
    resources/themes/polished/sliderbg-hw.png \
    resources/themes/polished/sliderbg-v-disabled.png \
    resources/themes/polished/sliderbg-v.png \
    resources/themes/polished/sliderbg-ve-disabled.png \
    resources/themes/polished/sliderbg-ve.png \
    resources/themes/polished/sliderbg-vw-disabled.png \
    resources/themes/polished/sliderbg-vw.png \
    resources/themes/polished/sort-arrow-disabled.gif \
    resources/themes/polished/sort-arrow-down.gif \
    resources/themes/polished/sort-arrow-none.gif \
    resources/themes/polished/sort-arrow-up.gif \
    resources/themes/polished/splitter-h.png \
    resources/themes/polished/splitter-v.png \
    resources/themes/polished/stripes/generate.sh \
    resources/themes/polished/stripes/stripe-10px.gif \
    resources/themes/polished/stripes/stripe-11px.gif \
    resources/themes/polished/stripes/stripe-12px.gif \
    resources/themes/polished/stripes/stripe-13px.gif \
    resources/themes/polished/stripes/stripe-14px.gif \
    resources/themes/polished/stripes/stripe-15px.gif \
    resources/themes/polished/stripes/stripe-16px.gif \
    resources/themes/polished/stripes/stripe-17px.gif \
    resources/themes/polished/stripes/stripe-18px.gif \
    resources/themes/polished/stripes/stripe-19px.gif \
    resources/themes/polished/stripes/stripe-20px.gif \
    resources/themes/polished/stripes/stripe-21px.gif \
    resources/themes/polished/stripes/stripe-22px.gif \
    resources/themes/polished/stripes/stripe-23px.gif \
    resources/themes/polished/stripes/stripe-24px.gif \
    resources/themes/polished/stripes/stripe-25px.gif \
    resources/themes/polished/stripes/stripe-26px.gif \
    resources/themes/polished/stripes/stripe-27px.gif \
    resources/themes/polished/stripes/stripe-28px.gif \
    resources/themes/polished/stripes/stripe-29px.gif \
    resources/themes/polished/stripes/stripe-30px.gif \
    resources/themes/polished/stripes/stripe-31px.gif \
    resources/themes/polished/stripes/stripe-32px.gif \
    resources/themes/polished/stripes/stripe-33px.gif \
    resources/themes/polished/stripes/stripe-34px.gif \
    resources/themes/polished/stripes/stripe-35px.gif \
    resources/themes/polished/stripes/stripe-36px.gif \
    resources/themes/polished/stripes/stripe-37px.gif \
    resources/themes/polished/stripes/stripe-38px.gif \
    resources/themes/polished/stripes/stripe-39px.gif \
    resources/themes/polished/stripes/stripe-40px.gif \
    resources/themes/polished/suggest-dropdown.png \
    resources/themes/polished/title-gradient.png \
    resources/themes/polished/wt.css \
    resources/themes/polished/wt_ie.css \
    resources/themes/polished/wt_ie6.css \
    resources/transitions.css \
    resources/tv-line-last-rtl.gif \
    resources/tv-line-last.gif \
    resources/webkit-transitions.css \
    strings-ru.xml \
    strings.xml \
    style.astylerc \
    wt_config.xml

HEADERS += \
    ap_application.h \
    ap_session.h \
    ap_user.h \
    config.h \
    dbase.h \
    dbodefs.h \
    embeddableapp.h \
    imageprocessor.h \
    sh_application.h \
    sh_business.h \
    sh_persistdata.h \
    tools.h \
    wthelpers.h

INCLUDEPATH += /usr/include/GraphicsMagick/

# DEFINES += MAGICKCORE_HDRI_ENABLE=1
# DEFINES += MAGICKCORE_QUANTUM_DEPTH=16
# DEFINES += MAGICKCORE_CHANNEL_MASK_DEPTH=32

QMAKE_CXXFLAGS += -Ofast
QMAKE_CXXFLAGS += -march=native
QMAKE_CXXFLAGS += -msse4.2
QMAKE_CXXFLAGS += -fopenmp

# QMAKE_CXXFLAGS += -fopenmp

unix:!macx: LIBS += -lpthread
unix:!macx: LIBS += -lssl
unix:!macx: LIBS += -lcrypto
unix:!macx: LIBS += -lcryptopp
unix:!macx: LIBS += -lz
unix:!macx: LIBS += -lboost_program_options
unix:!macx: LIBS += -lboost_filesystem
unix:!macx: LIBS += -lboost_thread
unix:!macx: LIBS += -lwt
unix:!macx: LIBS += -lwtdbo
unix:!macx: LIBS += -lwtdbosqlite3
unix:!macx: LIBS += -lwthttp

unix:!macx: LIBS += -lGraphicsMagick++
unix:!macx: LIBS += -lGraphicsMagick
unix:!macx: LIBS += -lGraphicsMagickWand
