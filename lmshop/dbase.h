#pragma once
#ifndef DBASE_H
#define DBASE_H

#include <Wt/Dbo/Dbo.h>
#include <string>
#include <optional>
#include <chrono>
#include <vector>

namespace dbo = Wt::Dbo;
using timestamp = std::chrono::system_clock::time_point;
template<class T> using dbo_ptr = dbo::ptr<T>;
template<class T> using dbo_ptr_collection = dbo::collection<dbo::ptr<T>>;

class DbItem;
class Category;
class Product;
class AvailableSize;
class Attribute;
class Image;
class Order;

#define CATEGORY "category"
#define CATEGORIES_PRODUCTS "categories_products"
#define PRODUCT "product"
#define SQLITE_DBASE "lmshop.db"

enum class ImageFormat : int {
    JPEG,   // jpeg
    PNG,    // png
    GIF     // gif
};

enum class CategoryKind : int {
    ProductTaxonomy // классификация товаров в магазине
};

class DbItem {
  public:
    timestamp created_at {std::chrono::system_clock::now()};    // когда создан
    std::optional<timestamp> updated_at;                        // когда изменен

  protected:
    template<class Action> void persist(Action &a) {
        dbo::field(a, created_at, "created_at");
        dbo::field(a, updated_at, "updated_at");
    }
};

class Category: virtual public DbItem {
  public:
    CategoryKind kind = CategoryKind::ProductTaxonomy;  // назначение категории
    std::string title;                                  // название
    std::optional<std::string> description;             // описание
    dbo_ptr<Category> category;                         // объемлющая категория
    dbo_ptr_collection<Category> categories;            // вложенные категории
    dbo_ptr_collection<Product> products;               // товары

    template<class Action> void persist(Action &a) {
        dbo::field(a, kind, "kind");
        dbo::field(a, title, "title");
        dbo::field(a, description, "description");
        dbo::belongsTo(a, category, CATEGORY);
        dbo::hasMany(a, categories, dbo::ManyToOne, CATEGORY);
        dbo::hasMany(a, products, dbo::ManyToMany, CATEGORIES_PRODUCTS);
        DbItem::persist(a);
    }
};

namespace Wt {
namespace Dbo {

/*
 * Переопределяем параметры идентификатора для Product:
 * используем поле article как идентификатор
*/

template<>
struct dbo_traits<Product>: public dbo_default_traits {
    using IdType = std::string;
    static constexpr IdType invalidId() noexcept {
        return {};
    }
    static constexpr const char *surrogateIdField() noexcept {
        return nullptr;
    }
};

}
}

class Product: virtual public DbItem {
  public:
    std::string article;                                        // внутренний артикул, он же идентификатор
    std::string title;                                          // название
    std::optional<std::string> description;                     // описание
    std::optional<std::string> color;                           // цвет
    int actual_price;                                           // цена в копейках
    std::optional<int> old_price;                               // старая цена в копейках
    int sales_quantity;                                         // количество продаж
    std::optional<timestamp> published_at = created_at;         // время публикации (опубликован, если published_at > now())
    dbo_ptr_collection<Category> categories;                    // категории
    dbo_ptr_collection<AvailableSize> sizes;                    // размеры в наличии
    dbo_ptr_collection<Image> images;                           // изображения
    dbo_ptr_collection<Order> orders;                           // заказы

    template<class Action> void persist(Action &a) {
        dbo::id(a, article, "article");
        dbo::field(a, title, "title");
        dbo::field(a, description, "description");
        dbo::field(a, color, "color");
        dbo::field(a, actual_price, "actual_price");
        dbo::field(a, old_price, "old_price");
        dbo::field(a, sales_quantity, "sales_quantity");
        dbo::field(a, published_at, "published_at");
        dbo::hasMany(a, categories, dbo::ManyToMany, CATEGORIES_PRODUCTS);
        dbo::hasMany(a, sizes, dbo::ManyToOne, PRODUCT);
        dbo::hasMany(a, images, dbo::ManyToOne, PRODUCT);
        dbo::hasMany(a, orders, dbo::ManyToOne, PRODUCT);
        DbItem::persist(a);
    }
};

class AvailableSize: virtual public DbItem {
  public:
    std::string size;           // размер
    int quantity;               // количество в наличии
    dbo_ptr<Product> product;   // товар

    template<class Action> void persist(Action &a) {
        dbo::field(a, size, "size");
        dbo::field(a, quantity, "quantity");
        dbo::belongsTo(a, product, PRODUCT);
        DbItem::persist(a);
    }
};

class Attribute: virtual public DbItem {
  public:
    std::string name;           // имя атрибута
    std::string value;          // значение атрибута
    dbo_ptr<Product> product;   // товар

    template<class Action> void persist(Action &a) {
        dbo::field(a, name, "name");
        dbo::field(a, value, "value");
        dbo::belongsTo(a, product, PRODUCT);
        DbItem::persist(a);
    }
};

class Image: virtual public DbItem {
  public:
    bool primary;                                           // основное изображение?
    ImageFormat format;                                     // формат картинки
    std::vector<unsigned char> data;                        // данные
    std::optional<std::vector<unsigned char>> thumbnail;    // миниатюра
    dbo_ptr<Product> product;                               // товар

    template<class Action> void persist(Action &a) {
        dbo::field(a, primary, "primary");
        dbo::field(a, format, "format");
        dbo::field(a, data, "data");
        dbo::field(a, thumbnail, "thumbnail");
        dbo::belongsTo(a, product, PRODUCT);
        DbItem::persist(a);
    }
};

class Order: virtual public DbItem {
  public:
    std::string scart_uuid;     // ид.корзины
    std::string size;           // размер
    int quantity;               // количество
    dbo_ptr<Product> product;   // заказанный товар

    template<class Action> void persist(Action &a) {
        dbo::field(a, scart_uuid, "scart_uuid");
        dbo::field(a, size, "size");
        dbo::field(a, quantity, "quantity");
        dbo::belongsTo(a, product, PRODUCT);
        DbItem::persist(a);
    }
};

#undef CATEGORY
#undef CATEGORIES_PRODUCTS
#undef PRODUCT

class Db final {
  public:
    static dbo::Session &session() {
        return _session;
    }

  private:
    static bool _initiated;
    static dbo::Session _session;
};

#endif // DBASE_H
