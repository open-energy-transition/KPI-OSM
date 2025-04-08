[out:json][timeout:400]; 
          relation["boundary"="administrative"][~"^name(:en)?$"~"${country}", i] -> .admin_boundary;
          .admin_boundary map_to_area -> .searchArea;
          
          node["power"="tower"](area.searchArea) -> .towers;
          node["power"="pole"](area.searchArea) -> .poles;
          way["power"="line"](area.searchArea)(bn.towers) -> .lines_connected;
          way["power"="line"]["voltage"](if:t["voltage"] >= 90000)(area.searchArea) -> .high_voltage_lines;
          node.poles(w.high_voltage_lines) -> .hv_poles;
          
          (
            node.towers(user_touched:${userFilter});
            node.hv_poles(user_touched:${userFilter});
          ) -> .my_nodes;
          
          way["power"="line"](bn.my_nodes) -> .connected_ways;
          
          (
            .my_nodes;
            .connected_ways;
          );
          
          out body;
          >;
          out skel qt;
