#include "business.h"
#include <Wt/WException.h>

namespace {

template<typename T>
inline auto create(std::unique_ptr<T> p) {
    if (Business::validate(*p)) {
        dbo::Transaction _(Db::session());
        return Db::session().add(std::move(p));
    } else {
        throw Wt::WException("");
    }
}

template<typename T>
inline dbo_ptr<T> update(dbo_ptr<T> p, const T &s) {
    if (Business::validate(s)) {
        dbo::Transaction _(Db::session());
        *p.modify() = s;
        return p;
    } else {
        throw Wt::WException("");
    }
}

template<typename T>
inline void remove(dbo_ptr<T> p) {
    dbo::Transaction _(Db::session());

    if (Business::is_removable(p)) {
        p.remove();
    } else {
        throw Wt::WException("");
    }
}

}

CategoryPtr Business::createCategory(std::unique_ptr<Category> category) {
    return create(std::move(category));
}

CategoryPtr Business::findCategory(int category_id) {

}

CategoryPtr Business::updateCategory(CategoryPtr category, const Category &source) {
    return update(category, source);
}

void Business::deleteCategory(CategoryPtr category) {
    remove(category);
}

ProductPtr Business::createProduct(std::unique_ptr<Product> product) {
    return create(std::move(product));
}

ProductPtr Business::findProduct(const std::string &article) {

}

ProductPtr Business::updateProduct(ProductPtr product, const Product &source) {
    return update(product, source);
}

void Business::deleteProduct(ProductPtr product) {
    remove(product);
}

AttributePtr Business::createAttribute(std::unique_ptr<Attribute> attribute) {
    return create(std::move(attribute));
}

AttributePtr Business::findAttribute(int attribute_id) {

}

AttributePtr Business::updateAttribute(AttributePtr attribute, const Attribute &source) {
    return update(attribute, source);
}

void Business::deleteAttribute(AttributePtr attribute) {
    remove(attribute);
}

AvailableSizePtr Business::createAvailableSize(std::unique_ptr<AvailableSize> available_size) {
    return create(std::move(available_size));
}

AvailableSizePtr Business::findAvailableSize(int available_size_id) {

}

AvailableSizePtr Business::updateAvailableSize(AvailableSizePtr available_size, const AvailableSize &source) {
    return update(available_size, source);
}

void Business::deleteAvailableSize(AvailableSizePtr available_size) {
    remove(available_size);
}

ImagePtr Business::createImage(std::unique_ptr<Image> image) {
    return create(std::move(image));
}

ImagePtr Business::findImage(int image_id) {

}

ImagePtr Business::updateImage(ImagePtr image, const Image &source) {
    return update(image, source);
}

void Business::deleteImage(ImagePtr image) {
    remove(image);
}

OrderPtr Business::createOrder(std::unique_ptr<Order> order) {
    return create(std::move(order));
}

OrderPtr Business::findOrder(int order_id) {

}

OrderPtr Business::updateOrder(OrderPtr order, const Order &source) {
    return update(order, source);
}

void Business::deleteOrder(OrderPtr order) {
    remove(order);
}

bool Business::validate(const Category &category) {
    return true; //TODO implement
}

bool Business::validate(const Product &product) {
    return true; //TODO implement
}

bool Business::validate(const Attribute &attribute) {
    return true; //TODO implement
}

bool Business::validate(const AvailableSize &available_size) {
    return true; //TODO implement
}

bool Business::validate(const Image &image) {
    return true; //TODO implement
}

bool Business::validate(const Order &order) {
    return true; //TODO implement
}

bool Business::is_removable(CategoryPtr category) {
    return true; //TODO implement
}

bool Business::is_removable(ProductPtr product) {
    return true; //TODO implement
}

bool Business::is_removable(AttributePtr attribute) {
    return true; //TODO implement
}

bool Business::is_removable(AvailableSizePtr available_size) {
    return true; //TODO implement
}

bool Business::is_removable(ImagePtr image) {
    return true; //TODO implement
}

bool Business::is_removable(OrderPtr order) {
    return true; //TODO implement
}
