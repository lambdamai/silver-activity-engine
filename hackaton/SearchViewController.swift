import UIKit

class SearchViewController: UIViewController {
    
    @IBOutlet weak var searchButton: UIButton!
    @IBOutlet weak var searchTextField: UITextField!
    @IBOutlet weak var searchTableView: UITableView!
    @IBAction func findButtonTapped(_ sender: Any) {
        if searchTextField.text == "2301039358" {
            organization = Organization(title: "ООО \" Эрик \"",
                                        link: "/id/183960",
                                        head_title: "директор",
                                        head_name: "Залян Толик Гришаевич",
                                        inn: "2301039358",
                                        ogrn: "1022300515511",
                                        reg_date: "25 октября 1999 г.",
                                        reg_cap: "10 000 руб.",
                                        status: nil,
                                        main_activity: "47.75 Торговля розничная косметическими и товарами личной гигиены в специализированных магазинах",
                                        main_activity_code: "477500",
                                        address: "353411, Краснодарский край, Анапский район, село Супсех, Советская улица, дом 70")
            searchTableView.reloadData()
            self.view.endEditing(true)
        } else {
            organization = nil
        }
    }
    
    var organization: Organization?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        searchTableView.delegate = self
        searchTableView.dataSource = self
        
        Gradient().setGradientToNavigationBar(viewController: self)
        
        searchButton.layer.cornerRadius = 5
    }
}

extension SearchViewController: UITableViewDataSource, UITableViewDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 11
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let row = indexPath.row
        var cell: UITableViewCell
        if row == 10 {
            cell = tableView.dequeueReusableCell(withIdentifier: "activityCell")!
        } else {
            cell = tableView.dequeueReusableCell(withIdentifier: "cell")!
        }
        cell.textLabel?.text = ""
        cell.detailTextLabel?.text = ""
        if organization != nil {
            switch row {
            case 0:
                cell.detailTextLabel?.text = organization?.title
            case 1:
                cell.textLabel?.text = "ИНН:"
                cell.detailTextLabel?.text = organization?.inn
            case 2:
                cell.textLabel?.text = "ОГРН:"
                cell.detailTextLabel?.text = organization?.ogrn
            case 3:
                cell.textLabel?.text = "дата регистрации"
                cell.detailTextLabel?.text = organization?.reg_date
            case 4:
                cell.textLabel?.text = organization?.head_title
                cell.detailTextLabel?.text = organization?.head_name
            case 5:
                cell.textLabel?.text = "уставный капитал"
                cell.detailTextLabel?.text = organization?.reg_cap
            case 6:
                cell.textLabel?.text = "основной вид деятельности"
                cell.detailTextLabel?.text = organization?.main_activity
            case 8:
                cell.textLabel?.text = "адресс"
                cell.detailTextLabel?.text = organization?.address
            case 7:
                if organization?.status != nil {
                    cell.textLabel?.text = "статус:"
                    cell.detailTextLabel?.text = organization?.status
                }
            case 10:
                cell.backgroundColor = #colorLiteral(red: 0.1077323332, green: 0.2683261633, blue: 0.9990518689, alpha: 1)
                cell.textLabel?.textColor = .white
                cell.textLabel?.font = UIFont(name: (cell.textLabel?.font.fontName)!, size: 15)
                cell.textLabel?.text = "Активность в социальных сетях"
            default: print("----")
            }
        }
        return cell
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        self.view.endEditing(true)
        if organization != nil && indexPath.row == 10 {
            self.performSegue(withIdentifier: "socialInfo", sender: self)
        }
    }
}
