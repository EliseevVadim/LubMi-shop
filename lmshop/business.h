#ifndef BUSINESS_H
#define BUSINESS_H

#include "dbase.h"
#include <string>
#include <memory>

using CategoryPtr = dbo_ptr<Category>;
using ProductPtr = dbo_ptr<Product>;
using AvailableSizePtr = dbo_ptr<AvailableSize>;
using AttributePtr = dbo_ptr<Attribute>;
using ImagePtr = dbo_ptr<Image>;
using OrderPtr = dbo_ptr<Order>;

class Business {
  public:
    static CategoryPtr createCategory(std::unique_ptr<Category> category);
    static CategoryPtr findCategory(int category_id);
    static CategoryPtr updateCategory(CategoryPtr category, const Category &source);
    static void deleteCategory(CategoryPtr category);

    static ProductPtr createProduct(std::unique_ptr<Product> product);
    static ProductPtr findProduct(const std::string &article);
    static ProductPtr updateProduct(ProductPtr product, const Product &source);
    static void deleteProduct(ProductPtr product);

    static AttributePtr createAttribute(std::unique_ptr<Attribute> attribute);
    static AttributePtr findAttribute(int attribute_id);
    static AttributePtr updateAttribute(AttributePtr attribute, const Attribute &source);
    static void deleteAttribute(AttributePtr attribute);

    static AvailableSizePtr createAvailableSize(std::unique_ptr<AvailableSize> available_size);
    static AvailableSizePtr findAvailableSize(int available_size_id);
    static AvailableSizePtr updateAvailableSize(AvailableSizePtr available_size, const AvailableSize &source);
    static void deleteAvailableSize(AvailableSizePtr available_size);

    static ImagePtr createImage(std::unique_ptr<Image> image);
    static ImagePtr findImage(int image_id);
    static ImagePtr updateImage(ImagePtr image, const Image &source);
    static void deleteImage(ImagePtr image);

    static OrderPtr createOrder(std::unique_ptr<Order> order);
    static OrderPtr findOrder(int order_id);
    static OrderPtr updateOrder(OrderPtr order, const Order &source);
    static void deleteOrder(OrderPtr order);

    static bool validate(const Category &category);
    static bool validate(const Product &product);
    static bool validate(const Attribute &attribute);
    static bool validate(const AvailableSize &available_size);
    static bool validate(const Image &image);
    static bool validate(const Order &order);

    static bool is_removable(CategoryPtr category);
    static bool is_removable(ProductPtr product);
    static bool is_removable(AttributePtr attribute);
    static bool is_removable(AvailableSizePtr available_size);
    static bool is_removable(ImagePtr image);
    static bool is_removable(OrderPtr order);
};

#endif // BUSINESS_H
