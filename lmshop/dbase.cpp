#include "dbase.h"
#include <memory>
#include <iostream>
#include <format>
#include <Wt/Dbo/backend/Sqlite3.h>

dbo::Session Db::_session {};

bool Db::_initiated = []()->bool{
    Db::session().setConnection(std::make_unique<dbo::backend::Sqlite3>(LMSHOP_DBASE));
    Db::session().mapClass<Category>("tab_category");
    Db::session().mapClass<Product>("tab_product");
    Db::session().mapClass<AvailableSize>("tab_available_size");
    Db::session().mapClass<Attribute>("tab_attribute");
    Db::session().mapClass<Image>("tab_image");
    Db::session().mapClass<Order>("tab_order");

    try {
        Db::session().createTables();
    } catch (const dbo::Exception &e) {
        std::cout << std::format("what: {}, code: {}", e.what(), e.code()) << std::endl;
    }

    return true;
}();
