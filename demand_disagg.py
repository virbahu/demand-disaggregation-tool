import numpy as np
def disaggregate(total_forecast, hierarchy, method="proportional"):
    results={}
    if method=="proportional":
        total_hist=sum(node["historical"] for node in hierarchy)
        for node in hierarchy:
            share=node["historical"]/max(total_hist,1)
            allocated=total_forecast*share
            results[node["name"]]=round(allocated,0)
    elif method=="weighted":
        weights=[node["historical"]*node.get("weight",1) for node in hierarchy]
        total_w=sum(weights)
        for i,node in enumerate(hierarchy):
            results[node["name"]]=round(total_forecast*weights[i]/max(total_w,1),0)
    diff=total_forecast-sum(results.values())
    if results and diff!=0:
        top=max(results,key=results.get); results[top]+=diff
    return results
def multi_level(forecasts, levels):
    final={}
    for level in levels:
        parent_fc=forecasts.get(level["parent"],0)
        children=level["children"]
        alloc=disaggregate(parent_fc,children)
        final.update(alloc)
        for name,qty in alloc.items(): forecasts[name]=qty
    return final
if __name__=="__main__":
    hierarchy=[{"name":"East-SKU-A","historical":300,"weight":1.2},
               {"name":"East-SKU-B","historical":200,"weight":1.0},
               {"name":"West-SKU-A","historical":350,"weight":1.1},
               {"name":"West-SKU-B","historical":150,"weight":0.8}]
    print(disaggregate(1200,hierarchy,"weighted"))
