#pragma once
#ifndef LMSHOPAPP_H
#define LMSHOPAPP_H

#include "embeddableapp.h"
#include "sh_persistdata.h"

class ShopApplication : public EmbeddableApp {
  public:
    ShopApplication(const Wt::WEnvironment &env, bool embedded = false);
      ~ShopApplication();
    void populateInterior() override;

  protected:
    std::string title() const override;

  private:

    std::list<Wt::Signals::connection> connections_;
      static Wt::Signal<const ShopApplication *, const std::string &> broadcast_message_; //TODO map of string -> signal
    PersistData _persist_data;
};

#endif // LMSHOPAPP_H
