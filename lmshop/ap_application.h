#pragma once
#ifndef APAPPLICATION_H
#define APAPPLICATION_H

#include "ap_session.h"
#include "embeddableapp.h"

class ApApplication : public EmbeddableApp {
  public:
    explicit ApApplication(const Wt::WEnvironment &env, bool embedded = false);
    void authEvent();

  private:
    ApSession session_;

  protected:
    std::string title() const override {
        return "AdminPanel";
    }

  public:
    void populateInterior() override;
};

#endif // APAPPLICATION_H
