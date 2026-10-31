package com.anomaly.backend.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "evaluation_log")
public class evaluation_log {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "channel")
    private String channel;

    @Column(name = "precision")
    private Double precision;

    @Column(name = "recall")
    private Double recall;

    @Column(name = "amount_flagged")
    private Integer amountFlagged;
}