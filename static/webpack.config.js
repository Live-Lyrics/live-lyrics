const webpack = require("webpack");
const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const CleanWebpackPlugin = require("clean-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");

module.exports = {
  entry: {
    main: "./js/main.js",
    lyrsense: "./js/lyrsense.js",
    vendor: ["axios"]
  },
  output: {
    filename: "./static/js/[name].bundle.js",
    path: path.resolve(__dirname, "dist")
  },
  module: {
    rules: [
      {
        test: /\.(html)$/,
        use: {
          loader: "html-loader",
          options: {
            attrs: [":data-src"],
          }
        }
      },
      {
        test: /\.css$/,
        use: ExtractTextPlugin.extract({
          fallback: "style-loader",
          use: "css-loader"
        })
      },
      {
        test: /\.handlebars$/,
        loader: "handlebars-loader"
      }
    ]
  },
  devtool: "inline-source-map",
  devServer: {
    contentBase: "./dist"
  },
  plugins: [
    new CleanWebpackPlugin(["dist"]),
    new HtmlWebpackPlugin({
      template: "index.html",
      filename: "templates/index.html"
    }),
    new ExtractTextPlugin("./static/css/[name].css"),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      "window.jQuery": "jquery"
    }),

    new webpack.optimize.CommonsChunkPlugin({
      name: "vendor"
    }),
    new webpack.optimize.CommonsChunkPlugin({
      name: "runtime"
    }),
    new CopyWebpackPlugin([{ from: "images", to: "static/images" }])
  ]
};
