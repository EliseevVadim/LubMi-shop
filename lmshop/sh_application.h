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
    std::unique_ptr<Wt::WContainerWidget> createHeader();
    std::unique_ptr<Wt::WContainerWidget> createFooter();
    std::unique_ptr<Wt::WContainerWidget> createMainPage();
    std::unique_ptr<Wt::WContainerWidget> createCataloguePage();
    std::unique_ptr<Wt::WContainerWidget> createPerfumeryPage();
    std::unique_ptr<Wt::WContainerWidget> createDeliveryPage();
    std::unique_ptr<Wt::WContainerWidget> createCarePage();
    std::unique_ptr<Wt::WContainerWidget> createContactsPage();
    std::unique_ptr<Wt::WContainerWidget> createAboutCompanyPage();
    std::unique_ptr<Wt::WContainerWidget> createUnderConstructionPage(const std::string &page_title);

    std::list<Wt::Signals::connection> connections_;
    static Wt::Signal<const ShopApplication *, const std::string &> broadcast_message_; //TODO map of string -> signal
    PersistData _persist_data;
};

#endif // LMSHOPAPP_H
