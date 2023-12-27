#ifndef LMSHOPAPP_H
#define LMSHOPAPP_H

#include "embeddableapp.h"
#include "dbase.h"
#include <pthread.h>
#include <shared_mutex>

class LmShopApp : public EmbeddableApp {
  public:
    LmShopApp(const Wt::WEnvironment &env, bool embedded = false);
    ~LmShopApp();
    void populateInterior() override;

  protected:
    std::string title() const override;

  private:
    std::list<Wt::Signals::connection> connections_;
    static Wt::Signal<const LmShopApp *, const std::string &> broadcast_message_;
};

#endif // LMSHOPAPP_H
