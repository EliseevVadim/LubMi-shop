#pragma once
#ifndef LMSHOPAPP_H
#define LMSHOPAPP_H

#include "embeddableapp.h"
#include "persistdata.h"

class LmShopApp : public EmbeddableApp {
  public:
    LmShopApp(const Wt::WEnvironment &env, bool embedded = false);
    ~LmShopApp();
    void populateInterior() override;

  protected:
    std::string title() const override;

  private:

    std::list<Wt::Signals::connection> connections_;
    static Wt::Signal<const LmShopApp *, const std::string &> broadcast_message_; //TODO map of string -> signal
    PersistData _persist_data;
};

#endif // LMSHOPAPP_H
