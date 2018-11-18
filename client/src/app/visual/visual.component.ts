import { Component, OnInit } from '@angular/core';
import * as d3 from "d3";

@Component({
  selector: 'app-visual',
  templateUrl: './visual.component.html',
  styleUrls: ['./visual.component.css']
})
export class VisualComponent implements OnInit {

  x: any;
  y: any;
  brush: any;
  dot: any;
  width: number;
  height: number;


  constructor() { }

  ngOnInit() {

    let brushcentered: (x,y,z) => void = () => {
      let dx = this.x(1) - this.x(0), // Use a fixed width when recentering.
        cx = d3.mouse(d3.event.currentTarget)[0],
        x0 = cx - dx / 2,
        x1 = cx + dx / 2;
      d3.select(d3.event.currentTarget.parentNode).call(this.brush.move, x1 > this.width ? [this.width - dx, this.width] : x0 < 0 ? [0, dx] : [x0, x1]);
    }

    let brushed: (xy,z) => void = () => {
      let self = this;
      let extent = d3.event.selection.map(this.x.invert, this.x);
      this.dot.classed("selected", function (d) { return extent[0] <= d[0] && d[0] <= extent[1]; });
    }

    let randomX = d3.randomUniform(0, 10);
    let randomY = d3.randomNormal(0.5, 0.12);
    let data = d3.range(800).map(function () { return [randomX(), randomY()]; });

    let svg = d3.select("svg")
    let margin = { top: 10, right: 10, bottom: 30, left: 10 };
    let g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    this.width = +svg.attr("width") - margin.left - margin.right;
    this.height = +svg.attr("height") - margin.top - margin.bottom;

    this.x = d3.scaleLinear()
      .domain([0, 10])
      .range([0, this.width]);

    this.y = d3.scaleLinear()
      .range([this.height, 0]);

    this.brush = d3.brushX()
      .extent([[0, 0], [this.width, this.height]])
      .on("start brush", brushed);

    let self = this;

    this.dot = g.append("g")
      .attr("fill-opacity", 0.2)
      .selectAll("circle")
      .data(data)
      .enter().append("circle")
      .attr("transform", function (d) { return "translate(" + self.x(d[0]) + "," + self.y(d[1]) + ")"; })
      .attr("r", 3.5);

    g.append("g")
      .call(this.brush)
      .call(this.brush.move, [3, 5].map(this.x))
      .selectAll(".overlay")
      .each(function (d: any) { d.type = "selection"; }) // Treat overlay interaction as move.
      .on("mousedown touchstart", brushcentered); // Recenter before brushing.

    g.append("g")
      .attr("transform", "translate(0," + this.height + ")")
      .call(d3.axisBottom(this.x));


  }

}
