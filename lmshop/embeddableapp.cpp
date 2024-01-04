#include "embeddableapp.h"
#include "config.h"
#include "tools.h"
#include <format>
#include <Wt/WBorderLayout.h>
#include <Wt/WContainerWidget.h>
#include <Wt/WBootstrap5Theme.h>
#include <Wt/WFitLayout.h>
#include <Wt/WHBoxLayout.h>
#include <Wt/WImage.h>
#include <Wt/WText.h>

EmbeddableApp::EmbeddableApp(const Wt::WEnvironment &env, bool embedded):
    Wt::WApplication(env),
    embedded_{embedded},
    animation_{Wt::AnimationEffect::SlideInFromTop, Wt::TimingFunction::EaseOut, ANIM_DUR} {

    using namespace Wt;
    using namespace std;

    static set<string> avail_langs { AVAIL_LANGS };
    auto lang = Tools::getStringOption(env, "lang").value_or(DEFAULT_LANG);
    messageResourceBundle().use(appRoot() + (avail_langs.contains(lang) ? format("strings-{}", lang) : "strings"s));
    setTheme(make_shared<WBootstrap5Theme>());

    if (!embedded_) {
        top_ = root();
    } else {
        auto wcw = make_unique<WContainerWidget>();
        top_ = wcw.get();

        if (auto div = Tools::getStringOption(env, "div"); div) {
            setJavaScriptClass(*div);
            bindWidget(std::move(wcw), *div);
            top_->decorationStyle().setBorder({BorderStyle::Solid, BorderWidth::Thin});
        } else {
            std::cerr << "Missing: parameter: 'div'" << std::endl;
            return;
        }
    }

    // auto fl = top_->setLayout(make_unique<WFitLayout>());
    // auto interior = make_unique<WBorderLayout>();
    // interior_ = interior.get();
    // fl->addItem(std::move(interior));
    enableUpdates();
}

void EmbeddableApp::populateInterior() {
    using namespace Wt;
    using namespace std;

    if (!embedded()) {
        setTitle(title());
    }

    // interior()->setSpacing(4);

    // header
    // auto header = make_unique<WContainerWidget>();
    // auto hblyt = make_unique<WHBoxLayout>();
    // hblyt->setDirection(LayoutDirection::LeftToRight);
    // hblyt->addWidget(make_unique<WImage>(IMAGE_LINK_"logo.svg"), 0, AlignmentFlag::Left);
    // hblyt->addSpacing(10);
    // auto text = hblyt->addWidget(make_unique<WText>(format(R"(<h2>{}</h2>)", title())));
    // hblyt->addStretch(1);
    // text->decorationStyle().setForegroundColor({CLR_HTEXT});
    // header->decorationStyle().setBackgroundColor({CLR_BKG_HDR});
    // header->setLayout(std::move(hblyt));
    // interior()->addWidget(std::move(header), LayoutPosition::North);
}
