import UIKit
import WebKit

class MapViewController: UIViewController, WKNavigationDelegate {
    var webView: WKWebView!
    
    @IBAction func reloadButtonPressed(_ sender: Any) {
        webView.reload() 
    }
    
    override func loadView() {
        webView = WKWebView()
        webView.navigationDelegate = self
        view = webView
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let url = URL(string: "https://ioscreator.com")!
        webView.load(URLRequest(url: url))
        
        Gradient().setGradientToNavigationBar(viewController: self)
        Gradient().setGradientToTabBar(viewController: self)
        self.tabBarController?.tabBar.unselectedItemTintColor = .white
    }
}
