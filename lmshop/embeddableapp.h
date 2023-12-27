#pragma once
#ifndef EMBEDDABLEAPP_H
#define EMBEDDABLEAPP_H

#include <Wt/WApplication.h>

class EmbeddableApp:
    public Wt::WApplication {

  public:

    explicit EmbeddableApp(const Wt::WEnvironment &env, bool embedded = false);
    virtual void populateInterior();

  private:

    Wt::WContainerWidget *top_ {nullptr};
    Wt::WBorderLayout *interior_ {nullptr};
    const bool embedded_ {false};
    const Wt::WAnimation animation_;

  protected:

    auto top() {
        return top_;
    }

    auto interior() {
        return interior_;
    }

    auto &animation() {
        return animation_;
    }

    auto embdedded() const {
        return embedded_;
    }

    virtual std::string title() const = 0;

  protected:

    void idleTimeout() override {
        quit();
    }
};

#endif // EMBEDDABLEAPP_H
